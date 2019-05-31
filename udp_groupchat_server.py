import socket
import threading
import logging
import datetime

FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)


class ChatUdpServer:
    def __init__(self, ip='127.0.0.1', port=9999, interval=10):
        self.addr = (ip, port)
        self.sock = socket.socket(type=socket.SOCK_DGRAM)
        self.event = threading.Event()
        self.clients = {}
        self.interval = interval

    def start(self):
        self.sock.bind(self.addr)
        threading.Thread(target=self.recv, name='recv').start()

    def recv(self):
        while not self.event.is_set():
            localset = set()
            data, raddr = self.sock.recvfrom(1024)  # data, raddr, blocking
            logging.info(data)
            logging.info(raddr)
            current = datetime.datetime.now().timestamp()  # float
            if data.strip() == b'^hb^':
                self.clients[raddr] = current
                continue
            elif data.strip() == b'quit':
                if raddr in self.clients:
                    self.clients.pop(raddr)
                continue
            self.clients[raddr] = current  # 只要有心跳或有效数据就刷新最后一次心跳时间
            msg = "ACK {}. from {}:{}".format(data, *raddr).encode()
            for c, stamp in self.clients.items():
                if current - stamp > self.interval:
                    localset.add(c)
                else:
                    self.sock.sendto(msg, c)
            for c in localset:
                self.clients.pop(c, None)

    def stop(self):
        for c in self.clients:
            self.sock.sendto(b'bye', c)
        self.sock.close()
        self.event.set()


def main():
    cs = ChatUdpServer()
    cs.start()
    while True:
        cmd = input(">>>")
        if cmd.strip() == 'quit':
            cs.stop()
            break
        logging.info(threading.enumerate())


if __name__ == '__main__':
    main()
