import socket

client = socket.socket()

client.connect(('15.75.', 19530))
while True:
    cmd = input("(quit退出)>>").strip()
    if len(cmd) == 0:
        continue
    if cmd == "quit":
        break
    client.send(cmd.encode())
    cmd_res = client.recv(1024)
    print(cmd_res.decode())

client.close()
