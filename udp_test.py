import socket

server = socket.socket(type=socket.SOCK_DGRAM)

addr = ('0.0.0.0', 9999)

server.bind(addr)  # 绑定本地地址

data, raddr = server.recvfrom(1024)

print(data)
print(raddr)

server.sendto(b'ack', raddr)






