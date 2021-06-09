import socket

sock = socket.socket()
sock.connect(('localhost', 4546))

while True:
    cmd = input(">>> ")
    sock.send(cmd.encode())

    data = sock.recv(1024)
    if data.decode() != "[EXECUTED]":
        print(data.decode())

sock.close()
