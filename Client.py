import socket
import sys


arg = sys.argv
arg = arg[1:]
# print(arg)

if arg == []:
    arg = sys.argv
    print("Non ha argomenti")
    exit()
else:
    pass


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "192.168.0.180"
server_port = 23

client_socket.connect((server_ip, server_port))
client_socket.send((" ".join(arg)).encode())
response = client_socket.recv(1024).decode()
print(response)

client_socket.close()
