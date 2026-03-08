import socket
import threading
print("Starting server... ")

HOST = '0.0.0.0'
PORT = 5050
client_id = 0


def handle_client(conn, addr, cid):
    print(f"Client {cid} connected from {addr}")

    data = conn.recv(1024)

    if data:
        message = data.decode()

        response = f"Client {cid}: {message.upper()}"

        conn.sendall(response.encode())
    conn.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"Server started. Listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()

    client_id += 1
    thread = threading.Thread(target=handle_client, args=(conn, addr, client_id)).start()
