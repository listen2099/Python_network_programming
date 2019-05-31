import socket
import threading
import logging

FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)


class ChatUdpClient:
    def __init__(self, rip='127.0.0.1', rport=9999):
        self.raddr = (rip, rport)
        self.sock = socket.socket(type=socket.SOCK_DGRAM)
        self.event = threading.Event()

    def start(self):
        self.sock.connect(self.raddr)
        threading.Thread(target=self.recv, name='recv').start()

    def recv(self):
        while not self.event.is_set():
            data, addr = self.sock.recvfrom(1024)
            # addr ?= raddr
            logging.info(data)

    def send(self, msg: str = 'quit'):
        self.sock.sendto(msg.encode(), self.raddr)

    def stop(self):
        self.sock.close()
        self.event.set()


def main():
    cc = ChatUdpClient()
    cc.start()

    while True:
        cmd = input('>>>>')
        if cmd.strip() == 'quit':
            cc.send()  # quit
            cc.stop()
            break
        logging.info(threading.enumerate())
        cc.send(cmd)


if __name__ == '__main__':
    main()
