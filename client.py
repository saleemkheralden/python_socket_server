import socket

HOST_IP = "127.0.0.1"
HOST_PORT = 80
client_recv_bytes = 1024

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.connect((HOST_IP, HOST_PORT))

# soc.send(b"hello")
menu = soc.recv(client_recv_bytes).decode()
print(menu)
print("print 'menu' to get the menu")

cmd = ""
while cmd != "8":

    cmd = input("Enter input> ")
    if cmd == 'menu':
        print(menu)
        continue

    soc.send(cmd.encode())

    data = soc.recv(client_recv_bytes).decode()
    print(data)





