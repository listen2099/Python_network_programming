import socketserver
import threading
import logging
import sys

FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)


class ChatHandler(socketserver.BaseRequestHandler):  # 每个请求对应一个hander实例
    clients = {}  # 类变量记录多个实例

    def setup(self):
        self.event = threading.Event()
        self.clients[self.client_address] = self.request

    def handle(self):
        print(self.request)
        print(self.client_address)
        print(self.server)
        print(self.__dict__)
        print(self.server.__dict__)
        while not self.event.is_set():
            data = self.request.recv(1024)  # 收到空byte说明对方断开
            if data == b'' or data == b'quit':
                break
            print(data, self.client_address)
            msg = "{}->ack".format(data).encode()
            for c in self.clients.values():
                c.send(msg)

    def finish(self):
        self.clients.pop(self.client_address)
        self.event.set()


server = socketserver.ThreadingTCPServer(('0.0.0.0', 9999), ChatHandler)
print(server)
threading.Thread(target=server.serve_forever, name='server').start()


def main():
    try:
        while True:
            cmd = input('>>>')
            if cmd.strip() == 'quit':
                server.server_close()
                break
    except Exception as e:
        logging.info(e)
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == '__main__':
    main()
