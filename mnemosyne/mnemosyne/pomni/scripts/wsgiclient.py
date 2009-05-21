import time, urllib

def parse_JSON(fileobj):
   import simplejson, time
   for data in fileobj:
       simplejson.loads(data)

if __name__ == "__main__":
    t1 = time.time()
    parse_JSON(urllib.urlopen("http://192.168.255.17:9999/10000"))
    print time.time()-t1

