import os
import socket
import cv2

SERVER_IP = "127.0.0.1"
SERVER_PORT = 4242
MAX_PAYLOAD = 65507
ADDR = (SERVER_IP, SERVER_PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cap = cv2.VideoCapture(0)

script_dir = os.path.dirname(os.path.abspath(__file__))
cascade_path = os.path.join(script_dir, 'haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier(cascade_path)

send_image_next = True


def send_text(msg: str):
    client_socket.sendto(b"TXT" + msg.encode(), ADDR)


def send_rect(x: int | float, y: int | float, w: int | float, h: int | float):
    payload = f"{x},{y},{w},{h}".encode()
    client_socket.sendto(b"REC" + payload, ADDR)


def send_image(frame):
    success, encoded = cv2.imencode(".jpg", frame)
    if success and len(encoded) <= MAX_PAYLOAD - 4:
        data = b"IMG" + encoded.tobytes()
        client_socket.sendto(data, ADDR)
    else:
        send_text("Frame too large, skipping")


while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: failed to capture image")
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (400, 300))
    grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        grayImg, scaleFactor=1.1, minNeighbors=5)
    if send_image_next:
        send_image(frame)
    elif len(faces) > 0:
        x, y, w, h = faces[0]
        send_rect(x, y, w, h)

    send_image_next = not send_image_next

cap.release()
cv2.destroyAllWindows()
