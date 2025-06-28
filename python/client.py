import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 4242

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1)

client_socket.sendto("Hello from Python!".encode(), (SERVER_IP, SERVER_PORT))

data, (recv_ip, recv_port) = client_socket.recvfrom(1024)
print(f"Received: '{data.decode()}' {recv_ip}:{recv_port}")
