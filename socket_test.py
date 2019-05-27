import socket

server = socket.socket()
server.bind(('192.168.11.198', 9999))
server.listen()

s, raddr = server.accept()  # wait

print(server)
print(s)
print(raddr)

while True:
    data = s.recv(1024)
    print(data)
    s.send('ack. {}'.format(data.decode(encoding='GBK')).encode(encoding='GBK'))


# s.close()
# server.close()


# 192.168.11.198
# 192.168.189.1
# 192.168.174.1


