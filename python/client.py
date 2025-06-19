import random
import socket
import cv2

SERVER_IP = "127.0.0.1"
SERVER_PORT = 4242
MAX_PAYLOAD = 65507

addr = (SERVER_IP, SERVER_PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cap = cv2.VideoCapture(0)


class MessageSender:
    def __init__(self, server_ip="127.0.0.1", server_port=4242):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_addr = (server_ip, server_port)
        self.packet_ids = {}
        self.max_retries = 3

    def send_message(self, header, payload, max_size=65507):
        if len(payload) > max_size - 4:
            raise ValueError("Payload too large")

        packet_id = random.randint(0, 65535)
        data = f"{header}{packet_id:04d}".encode("ascii") + payload

        retries = 0
        while retries < self.max_retries:
            self.socket.sendto(data, self.server_addr)

            # Esperar confirmación
            self.socket.settimeout(0.1)
            try:
                response, _ = self.socket.recvfrom(1024)
                if response.startswith(b"ACK") and int(
                        response[3:].decode()) == packet_id:
                    break
            except socket.timeout:
                retries += 1

        if retries >= self.max_retries:
            raise TimeoutError(
                f"No se pudo enviar el mensaje después de {
                    self.max_retries} intentos"
            )


def send_vec2_text(x: int | float, y: int | float):
    payload = f"{x},{y}".encode("ascii")
    client_socket.sendto(b"VEC2" + payload, addr)


while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: failed to capture image")
        break

    frame = cv2.resize(frame, (400, 300))
    frame = cv2.flip(frame, 1)

    success, encoded_frame = cv2.imencode(".jpg", frame)

    if success and len(encoded_frame) <= MAX_PAYLOAD - 4:
        coord1_x = 100.0
        coord1_y = 200.0
        sender = MessageSender()
        try:
            sender.send_message("IMG0", encoded_frame.tobytes())
            sender.send_message(
                "VEC2", f"{coord1_x},{coord1_y}".encode("ascii"))
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
    else:
        data = b"TXT0" + b"Frame too large, skipping"
        client_socket.sendto(data, addr)


cap.release()
cv2.destroyAllWindows()
