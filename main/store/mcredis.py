import json

from redis import StrictRedis

REDIS_URI = 'redis://127.0.0.1:6379/0'

class McRedis(object):
    def __init__(self, redis_uri):
        self._client = StrictRedis.from_url(redis_uri)

    def __getattr__(self, name):
        return getattr(self._client, name)
    
    def get(self, key):
        v = self._client.get(key)
        print("***********{}***************".format(v))
        if v:
            return v.decode("utf-8")
        else:
            return None

mc = McRedis(REDIS_URI) 
