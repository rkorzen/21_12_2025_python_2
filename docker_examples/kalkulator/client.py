import socket
import sys

HOST = 'localhost'
PORT = 5070


message = " ".join(sys.argv[1:]) or "1 2 +"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.sendall(message.encode())
data = client.recv(1024).decode()
print("Response: ", data)
client.close()