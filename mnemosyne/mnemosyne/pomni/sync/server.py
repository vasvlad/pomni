import SocketServer
import simplejson


class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        command = self.request.recv(1024).strip()
        if command == 'history':
            # get events from history table after last sync.
            # events = self.get_events()
            events = [
                {"time":123, "event":9, "side": "server", "id":"afdsdf3432das"},
                {"time":456, "event":13, "side": "server", "id":"a123df3432das"},
                {"time":789, "event":14, "side": "server", "id":"a1AAAA3432das"}
            ]
            self.request.send(simplejson.dumps(events))
        elif command == 'get_card':
            # get card from database and send only necessary fields.
            # card_id = self.request.recv(1024).strip()
            # card = self.get_card_by_id(id)
            card_id = self.request.recv(1024).strip()
            print "server: have to return card with id:", card_id
            card = {'id': "id", '_id': "_id", 'tags': "tag1, tag2", 'grade': 2,
                'easiness': 4, 'last_rep': 12345, 'next_rep': 4567}
            self.request.send(simplejson.dumps(card))
        elif command == 'get_fact':
            # get fact from database and send only necessary fields.
            # fact_id = self.request.recv(1024).strip()
            # fact = self.get_fact_by_id(fact_id)
            fact_id = self.request.recv(1024).strip()
            print "server: have to return fact with id:", fact_id
            fact = {'timestamp': 12345, 'cardtype': 3, \
                'fact':{'q':'simple question', 'a':'simple answer'}}
            self.request.send(simplejson.dumps(fact))
        elif command == 'get_tag':
            # get tag from database and send only necessary fields.
            # tag_id = self.request.recv(1024).strip()
            # tag = self.get_tag_by_id()
            tag_id = self.request.recv(1024).strip()
            print "server: have to return tag with id:", tag_id
            tag = {'name': "test_tag_name", 'extradata': 12345, 'id':tag_id}
            self.request.send(simplejson.dumps(tag))



if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    server.serve_forever()
