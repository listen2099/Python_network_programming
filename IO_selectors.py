import selectors
import socket
import threading
import logging
from queue import Queue

FORMAT = '%(asctime)s %(threadName)s %(thread)d %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


class ChatServer:
    def __init__(self, ip='0.0.0.0', port=9999):
        self.addr = (ip, port)
        self.sock = socket.socket()
        self.clients = {}  # 每个客户端的信息
        self.selector = selectors.DefaultSelector()

    def start(self):
        self.sock.bind(self.addr)
        self.sock.listen()
        self.sock.setblocking(False)
        # threading.Thread(target=self.accept).start()
        self.selector.register(self.sock, selectors.EVENT_READ | selectors.EVENT_WRITE, self.accept)

        threading.Thread(target=self._select, name='selector').start()

    def _select(self):
        while True:
            events = self.selector.select()
            for key, mask in events:
                if callable(key.data):
                    callback = key.data  # data = self.accept
                else:
                    callback = key.data[0]
                callback(key.fileobj, mask)  # self.accept(fobj, mask)

    def accept(self, sock, mask):
        newsock, raddr = self.sock.accept()  # blocking
        newsock.setblocking(True)
        self.clients[raddr] = (self.handle, Queue())
        # threading.Thread(target=self.recv, args=(newsock,)).start()
        self.selector.register(newsock, selectors.EVENT_READ | selectors.EVENT_WRITE, self.clients[raddr])

    def handle(self, newsock, mask):  # mask == 1, 2, 3
        if mask & selectors.EVENT_READ:
            data = newsock.recv(1024)
            if data == b'quit':
                self.selector.unregister(newsock)
                newsock.close()
                return
            # for key in self.selector.get_map().values():
            #     if key.data == self.recv:  # 一个sock受到数据,则使用所有sock发送数据
            #         key.fileobj.send(data)
            #         self.clients[key.fileobj.getpeername()].put(data)
            for q in self.clients.values():
                q.put(data)

        if mask & selectors.EVENT_WRITE:  # 2,0
            # 每一个sock对象本身只发送自己的数据
            raddr = newsock.getpeername()
            q = self.clients[raddr]
            if not q.empty():
                newsock.send(q.get())

    def stop(self):
        fileobjs = []
        for fd, key in self.selector.get_map().items():  # fd : key
            fileobjs.append(key.fileobj)
        for obj in fileobjs:
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
