import socket
import threading
import logging

FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)


class ChatUdpServer:
    def __init__(self, ip='127.0.0.1', port=9999):
        self.addr = (ip, port)
        self.sock = socket.socket(type=socket.SOCK_DGRAM)
        self.event = threading.Event()
        self.clients = set()

    def start(self):
        self.sock.bind(self.addr)
        threading.Thread(target=self.recv, name='recv').start()

    def recv(self):
        while not self.event.is_set():
            data, raddr = self.sock.recvfrom(1024)  # data, raddr, blocking
            logging.info(data)
            logging.info(raddr)
            if data.strip() == b'quit':
                if raddr in self.clients:
                    self.clients.remove(raddr)
                continue
            self.clients.add(raddr)
            msg = "ACK {}. from {}:{}".format(data, *raddr).encode()
            for c in self.clients:
                self.sock.sendto(msg, c)

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
