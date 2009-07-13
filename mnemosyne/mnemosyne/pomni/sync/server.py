import SocketServer
import simplejson

def generateJSON(param):
    data = {"time":1, "event":2, "id":"3", "side":[4]}
    return simplejson.dumps(data)


class MyTCPHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        #print "Handler.setup()"
        pass

    def handle(self):
        #print "Handler.handle()"
        command = self.request.recv(1024).strip()
        if command == 'history':
            data = [
                {"time":123, "event":12, "side": "server", "id":"afdsdf3432das"},
                {"time":456, "event":9, "side": "server", "id":"a123df3432das"}
            ]
            self.request.send(simplejson.dumps(data))

    def finish(self):
        #print "Handler.finish()"
        pass


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
