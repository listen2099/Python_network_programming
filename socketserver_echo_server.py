import socketserver
import threading
import logging
import sys

FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)


class EchoHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print(self.request)
        print(self.client_address)
        print(self.server)
        print(self.__dict__)
        print(self.server.__dict__)
        for i in range(3):
            data = self.request.recv(1024)
            print(data, self.client_address)
            msg = "{}->ack".format(data).encode()
            self.request.send(msg)


def main():
    server = socketserver.TCPServer(('0.0.0.0', 9999), EchoHandler)
    print(server)
    threading.Thread(target=server.serve_forever, name='server').start()
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
