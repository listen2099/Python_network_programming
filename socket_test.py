import socket

server = socket.socket()
server.bind(('0.0.0.0', 9999))
server.listen()

s, raddr = server.accept()  # wait

while True:
    data = s.recv(1024)
    print(data)
    s.send('ack. {}'.format(data.decode(encoding='utf-8')).encode(encoding='utf-8'))

s.close()
server.close()




