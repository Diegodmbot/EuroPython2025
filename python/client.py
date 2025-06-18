import socket
import cv2

server_ip = "127.0.0.1"
server_port = 4242

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cap = cv2.VideoCapture(0)

while True:    
    ret, frame = cap.read()

    if not ret:
        print("Error: failed to capture image")
        break

    frame = cv2.resize(frame, (400, 300))
    frame = cv2.flip(frame, 1)
    
    success, encoded_frame = cv2.imencode(".jpg", frame)

    if success and len(encoded_frame) <= 65507 - 4:
        data = b"IMG" + encoded_frame.tobytes()
    else:
        data = b"TXT" + b"Frame too large, skipping"

    client_socket.sendto(data, (server_ip, server_port))

cap.release()
cv2.destroyAllWindows()
