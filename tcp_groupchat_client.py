import socket
import threading
import logging

FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)


class ChatClient:
    def __init__(self, rip='192.168.11.198', rport=9999):
        self.raddr = (rip, rport)
        self.sock = socket.socket()
        self.event = threading.Event()

    def start(self):
        self.sock.connect(self.raddr)

        threading.Thread(target=self.recv, name='recv').start()

    def recv(self):
        while not self.event.is_set():
            data = self.sock.recv(1024)
            logging.info(data)

    def send(self, msg):
        self.sock.send('{}\n'.format(msg).encode())

    def stop(self):
        self.sock.close()
        self.event.set()


def main():

    cc = ChatClient()
    cc.start()

    while True:
        cmd = input('>>>')
        if cmd.strip() == 'quit':
            cc.stop()
            break
        cc.send(cmd)
        logging.info(threading.enumerate())


if __name__ == '__main__':
    main()
