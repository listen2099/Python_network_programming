import socketserver

class MyHandler(socketserver.BaseRequestHandler):
    def setup(self):
        pass
    def handle(self):  # recv
        print(self.request)  # new socket 用来recv
        print(self.client_address)  # raddr
        print(self.server)  # server
        print(self.__dict__)
        for i in range(3):
            data = self.request.recvfrom(1024)
            print(data, self.client_address)
    def finish(self):
        pass

#server = socketserver.ThreadingTCPServer(('0.0.0.0', 9999), MyHandler)
server = socketserver.TCPServer(('0.0.0.0', 9999), MyHandler)

server.serve_forever()











