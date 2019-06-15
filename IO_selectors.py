import selectors
import socket
import threading
import logging

FORMAT = '%(asctime)s %(threadName)s %(thread)d %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


class ChatServer:
    def __init__(self, ip='0.0.0.0', port=9999):
        self.addr = (ip, port)
        self.sock = socket.socket()

        self.selector = selectors.DefaultSelector()

    def start(self):
        self.sock.bind(self.addr)
        self.sock.listen()
        self.sock.setblocking(False)
        # threading.Thread(target=self.accept).start()
        self.selector.register(self.sock, selectors.EVENT_READ, self.accept)

        threading.Thread(target=self._select).start()

    def _select(self):
        while True:
            events = self.selector.select()
            logging.info(threading.enumerate())
            for key, mask in events:
                callback = key.data  # data = self.accept
                callback(key.fileobj)  # self.accept(fobj, mask)

    def accept(self, sock):
        newsock, raddr = self.sock.accept()  # blocking
        newsock.setblocking(False)
        # threading.Thread(target=self.recv, args=(newsock,)).start()
        self.selector.register(newsock, selectors.EVENT_READ | selectors.EVENT_WRITE, self.recv)

    def recv(self, newsock):
        data = newsock.recv(1024)
        if data == b'quit':
            self.selector.unregister(newsock)
            newsock.close()
            return
        newsock.send(data)

    def stop(self):
        fileonjs = []
        for fd, key in self.selector.get_map().items():  # fd : key
            fileonjs.append(key.fileobj)
        for obj in fileonjs:
            self.selector.unregister(obj)
            obj.close()
        self.selector.close()


if __name__ == '__main__':
    cs = ChatServer()
    cs.start()
    while True:
        cmd = input('>>>')
        if cmd.strip() == 'quit':
            cs.stop()
            break
        logging.info(threading.enumerate())
