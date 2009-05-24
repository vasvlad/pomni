import os, sys, random, time, urllib, httplib, urlparse
import simplejson

def parse_JSON(fileobj):
    i = 0
    for data in os.fdopen(fileobj.fileno(), 'rb', -1):
        simplejson.loads(data)
        i += 1
    return i

def parse_XML(fileobj): # Incrementally.
    from xml.etree.cElementTree import iterparse
    context = iterparse(fileobj, events=("end",))
    i = 0
    for event, elem in context:
        if event == "end" and elem.tag == "card":
            data = dict(elem.items()).values()
            for j in [0, 2, 3, 5, 6, 7, 8, 10, 13, 14, 15, 16, 17]:
                data[j] = int(data[j])
            for j in [4, 11, 12]:
                data[j] = float(data[j])
            i += 1
    return i

def randstr(length):
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') \
           for i in xrange(length)])

def generate_JSON(cards=10000):
    for cardid in xrange(cards):
        data = [cardid, randstr(40), cardid, cardid,
            random.randint(1,5), str(2.5),random.randint(1,100), str(0), str(0), str(10),
            str(0.0), str(0.0), str(1), randstr(40), str(10), str(1), str(1), str(1),
            randstr(40), randstr(40)]
        yield "%s\n" % simplejson.dumps(data)

def generate_XML(cards=10000):
    from xml.etree.cElementTree import Element, SubElement, tostring
    yield "<mnemosyne>"
    root = Element("mnemosyne")
    for cardid in xrange(cards):
        yield """<card _fact_id="%s" _id="%s" acq_reps="%s" acq_reps_since_lapse="%s" active="%s" easiness="%s" extra_data="%s" fact_view_id="%s" grade="%s" id="%s" in_view="%s" lapses="%s" last_rep="%s" needs_sync="%s" next_rep="%s" ret_reps="%s" seen_in_this_session="%s" unseen="%s"><q>%s</q><a>%s</a></card>""" % (cardid, randstr(40), cardid, cardid,
                    random.randint(1,5), str(2.5), random.randint(1,100),
                    str(0), str(0), str(10),
                    str(0.0), str(0.0), str(1),
                    randstr(40), str(10),
                    str(1), str(1), str(1), randstr(40), randstr(40))
    yield "</mnemosyne>"

def parse_uri(uri):
    scheme, netplace, path, query, fragid = urlparse.urlsplit(uri)

    if ':' in netplace: 
        host, port = netplace.split(':', 2)
        port = int(port)
    else: 
        host, port = netplace, 80

    if query: 
        path += '?' + query

    return host, port, path

def putdata(uri, iterator):
    host, port, path = parse_uri(uri)
    conn = httplib.HTTPConnection(host, port)
    conn.putrequest('POST', path)
    conn.putheader('User-Agent', 'gzip')
    conn.putheader('Accept-Encoding', 'gzip')
    conn.putheader('Connection', 'keep-alive')
    conn.putheader('Content-Type', 'text/plain')
    conn.putheader('Transfer-Encoding', 'chunked')
    conn.putheader('Expect', '100-continue')
    conn.putheader('Accept', '*/*')
    conn.endheaders()

    for chunk in iterator:
        length = len(chunk)
        conn.send('%X\r\n' % length)
        conn.send(chunk + '\r\n')
    conn.send('0\r\n\r\n')

    resp = conn.getresponse()
    body = resp.read()
    body = body.rstrip('\r\n')
    body = body.encode('string_escape')

    return (resp.status, body) # an int

from threading import Thread
from functools import wraps
def run_async(func):
    """
        run_async(func)
            function decorator, intended to make "func" run in a separate
            thread (asynchronously).
            Returns the created Thread object
    """
    
    @wraps(func)
    def async_func(*args, **kwargs):
        func_hl = Thread(target = func, args = args, kwargs = kwargs)
        func_hl.start()
        return func_hl

    return async_func

@run_async
def getcardsjson():
    t1 = time.time()
    cards = parse_JSON(urllib.urlopen("http://mnemosyneweb.appspot.com/sync/JSON"))
    print "getcards JSON: got %d cards from server in %f sec" % (cards, time.time()-t1)

@run_async
def putcardsjson():
    t1 = time.time()
    message = putdata("http://mnemosyneweb.appspot.com/sync/JSON", generate_JSON())
    print "putcards JSON: %s %f" % (message, time.time()-t1)

@run_async
def getcardsxml():
    t1 = time.time()
    cards = parse_XML(urllib.urlopen("http://mnemosyneweb.appspot.com/sync/XML"))
    print "getcards XML: got %d cards from server in %f sec" % (cards, time.time()-t1)

@run_async
def putcardsxml():
    t1 = time.time()
    message = putdata("http://mnemosyneweb.appspot.com/sync/XML", generate_XML())
    print "putcards XML: %s %f" % (message, time.time()-t1)

if __name__ == "__main__":
    getcardsjson()
    getcardsxml()
    putcardsjson()
    putcardsxml()

