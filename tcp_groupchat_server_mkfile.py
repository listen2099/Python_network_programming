import socket
import threading
import logging
import datetime

FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)

class ChatServer:
    def __init__(self, ip='192.168.11.198', port=9999):
        self.addr = (ip, port)
        self.sock = socket.socket()
        self.clients = {}
        self.event = threading.Event()

    def start(self):
        self.sock.bind(self.addr)
        self.sock.listen()

        threading.Thread(target=self.accept, name='accept').start()

    def accept(self):  # 一个线程
        while not self.event.is_set():
            s, raddr = self.sock.accept()  # block
            f = s.makefile(mode='rw')
            logging.info(f)
            logging.info(s)
            self.clients[raddr] = f
            threading.Thread(target=self.recv, name='recv', args=(f, raddr)).start()

    def recv(self, f, addr):  # 很多线程
        while not self.event.is_set():
            try:
                #data = sock.recv(1024)  # block
                data = f.readline()  # string 要有换行符
                logging.info(data)
            except Exception as e:
                logging.error(e)
                data = 'quit'
            if data == 'quit':
                self.clients.pop(addr)
                f.close()
                break
            msg = 'ack FROM {} in [{}]: {}'.format(
                addr,
                datetime.datetime.now().strftime('%Y/%m/%d-%H:%M:%S'),
                data)
            for f in self.clients.values():
                #  s.send(msg)
                f.write(msg)
                f.flush()

    def stop(self):
        for f in self.clients.values():
            f.close()
        self.sock.close()
        self.event.set()


cs = ChatServer()
cs.start()

while True:
    cmd = input('>>>')
    if cmd.strip() == 'quit':
        cs.stop()
        threading.Event.wait(3)
        break
    logging.info(threading.enumerate())


