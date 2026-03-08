import os
import socket
import threading

from service import CalculatorService

print("Starting server... ")

HOST = '0.0.0.0'
PORT = int(os.getenv("SERVER_PORT", 5050))


def handle_client(conn, addr):
    print(f"Client connected from {addr}")

    data = conn.recv(1024)

    if data:
        message = data.decode()

        a, b, op = message.split()
        a = int(a)
        b = int(b)
        response = CalculatorService.calculate(a, b, op)

        conn.sendall(str(response).encode())
    conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"Server started. Listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr)).start()
