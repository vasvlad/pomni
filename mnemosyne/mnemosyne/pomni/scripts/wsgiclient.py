import os, sys, random, time, urllib, httplib, urlparse
import simplejson

def parse_JSON(fileobj):
   for data in os.fdopen(fileobj.fileno(), 'rb', -1):
       simplejson.loads(data)

def parse_XML(fileobj): # Incrementally.
    from xml.etree.cElementTree import iterparse
    context = iterparse(fileobj, events=("start", "end"))
    root = None
    for event, elem in context:
        #print elem
        if event == "start" and root is None:
            root = elem     # The first element is root
        if event == "end" and elem.tag == "record":
          #... process record elements ...
          root.clear()

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
    conn.putheader('User-Agent', 'mnemosyne/2.0')
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

if __name__ == "__main__":
    t1 = time.time()
    #opener = urllib.FancyURLopener()
    #opener.addheader('User-Agent', 'gzip')
    #opener.addheader('Accept-Encoding', 'gzip')
    #opener.addheaders = [('Accept-encoding', 'gzip'), ('User-Agent', 'gzip')] 
    #urllib2.install_opener(opener)
    #parse_XML(opener.open("http://mnemosyneweb.appspot.com/XML"))
    #parse_JSON(opener.open("http://mnemosyneweb.appspot.com/JSON"))

    #parse_JSON(urllib.urlopen("http://localhost:8080/JSON"), data)
    #print putdata("http://localhost:8080/JSON", generate_JSON(3))
    print putdata("http://localhost:9999", generate_JSON(10000))
    print time.time()-t1

