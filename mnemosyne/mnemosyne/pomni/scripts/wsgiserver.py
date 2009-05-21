import time, random
from wsgiref.simple_server import make_server

def randstr(length):
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') \
            for i in xrange(length)])

def generate_JSON(cards=10000):
    import simplejson
    for cardid in xrange(cards):
        data = [cardid, randstr(40), cardid, cardid,
            random.randint(1,5), str(2.5),random.randint(1,100), str(0), str(0), str(10),
            str(0.0), str(0.0), str(1), randstr(40), str(10), str(1), str(1), str(1),
            randstr(40), randstr(40)]
        yield "%s\n" % simplejson.dumps(data)

def wsgi_application(environ, start_response):
    cards = int(environ['PATH_INFO'].split('/')[1])
    print "%s asked for %d cards" % (environ['REMOTE_ADDR'], cards)
    start_response('200 OK', [('Content-Type', 'text/json')])
    t1 = time.time()
    length = 0
    for chunk in generate_JSON(cards):
        yield chunk
        length += len(chunk)
    print time.time()-t1
    print length

httpd = make_server('', 9999, wsgi_application)
httpd.serve_forever()

