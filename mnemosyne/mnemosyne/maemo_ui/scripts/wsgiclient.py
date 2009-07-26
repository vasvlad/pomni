#!/usr/bin/python -tt
# vim: sw=4 ts=4 expandtab ai

# Author: Ed Bartosh <bartosh@gmail.com>

"""WSGI sync client for mnemosyne."""

import os, time, urllib, httplib, urlparse
from random import randint, choice

def randstr(length):
    return ''.join([choice('abcdefghijklmnopqrstuvwxyz') \
           for i in xrange(length)])

def parse_uri(uri):
    netplace, path, query = urlparse.urlsplit(uri)[1:4]

    if ':' in netplace: 
        host, port = netplace.split(':', 2)
        port = int(port)
    else: 
        host, port = netplace, 80

    if query: 
        path += '?' + query

    return host, port, path

def postdata(uri, iterator):
    """Post data incrementally using chunked HTTP POST."""

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
def getcards(urlp, proto, cards=10000):
    """Get cards from server and parse them."""
    
    def parse_json(fileobj):
        """Parse card info in JSON format."""
        import simplejson
        i = 0
        for data in os.fdopen(fileobj.fileno(), 'rb', -1):
            simplejson.loads(data)
            i += 1
        return i

    def parse_xml(fileobj): # Incrementally.
        """Parse card info in XML format."""

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

    start = time.time()
    
    cards = locals()["parse_%s" % proto.lower()](\
        urllib.urlopen("%s/%s?cards=%d" % (urlp, proto, cards)))

    print "getcards %s: got %d cards from server in %f sec" % \
        (proto, cards, time.time() - start)

@run_async
def sendcards(urlp, proto, cards=10000):
    """Send cards to the server."""

    def generate_xml(cards=cards):
        """Generate card info in XML format."""

        yield "<mnemosyne>"
        for cardid in xrange(cards):
            yield '<card _fact_id="%s" _id="%s" acq_reps="%s" '\
              'acq_reps_since_lapse="%s" active="%s" easiness="%s" '\
              'extra_data="%s" fact_view_id="%s" grade="%s" id="%s" '\
              'in_view="%s" lapses="%s" last_rep="%s" needs_sync="%s" '\
              'next_rep="%s" ret_reps="%s" seen_in_this_session="%s" '\
              'unseen="%s"><q>%s</q><a>%s</a></card>' % (cardid, randstr(40),
              cardid, cardid, randint(1,5), str(2.5),
              randint(1,100), str(0), str(0), str(10), str(0.0),
              str(0.0), str(1), randstr(40), str(10), str(1), str(1), str(1),
              randstr(40), randstr(40))
        yield "</mnemosyne>"

    def generate_json(cards=10000):

        """Generate card info in JSON format."""
        import simplejson
        for cardid in xrange(cards):
            data = [cardid, randstr(40), cardid, cardid,
                randint(1,5), str(2.5), randint(1,100), str(0), str(0), 
                str(10), str(0.0), str(0.0), str(1), randstr(40), str(10),
                str(1), str(1), str(1), randstr(40), randstr(40)]
            yield "%s\n" % simplejson.dumps(data)


    start = time.time()
    
    message = postdata("%s/%s" %(urlp, proto), 
                locals()["generate_%s" % proto.lower()](cards))
    
    print "putcards %s: %s took %f sec" % (proto, message, time.time() - start)

if __name__ == "__main__":
    URL = "http://mnemosyneweb.appspot.com/sync"
    getcards(URL, "JSON", 1000)
    getcards(URL, "XML", 1000)
    sendcards(URL, "JSON", 1000)
    sendcards(URL, "XML", 1000)

