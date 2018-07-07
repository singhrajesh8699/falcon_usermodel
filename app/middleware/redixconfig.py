
import falcon
import redis
import uuid

try:
    from Crypto.Random import get_random_bytes
    def getUuid():
        return uuid.UUID(bytes=get_random_bytes(16))

except ImportError:
    def getUuid():
        return uuid.uuid4()



class RedixDb(object):
    def __init__(self,host='localhost',port=6379,db=0):
        self.host = host
        self.port = port
        self.db = db
        self.connection_pool = None

    def process_request(self, req, resp):
        if self.connection_pool is None:
            self.connection_pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db)
        r = redis.Redis(connection_pool=self.connection_pool)
        req.context['redixdb'] = RedixSession(r,req, resp)


class RedixSession(object):

    def __init__(self,rdb,req=None,res=None):
        self.rdb = rdb
        self.req = req
        self.res = res
    
    def set_hashkey(self,hashkey,value):
        self.rdb.hset(hashkey,'id',value)
        self.rdb.expire(hashkey,3600)


    def __contains__(self,hashkey,key):
        return self.rdb.hexists(hashkey,key)
    

    def destroykey(self,hashkey,key):
        self.rdb.hdel(hashkey,key)
    

    def getvalue(self,hashkey,key):
        return self.rdb.hget(hashkey,key)