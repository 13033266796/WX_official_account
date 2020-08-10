import json

from redis import StrictRedis

REDIS_URI = 'redis://172.17.0.1:6379/0'

class McRedis(object):
    MESSAGE_ID_KEY = "OnlyU:{open_id}:message_id"

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

    def _message_repeat(self, open_id, message_id):
        if self._client.sismenber(MESSAGE_ID_KEY.format(open_id),
                                  message_id):
            return True

        return False

    def _save_messae(self, open_id, message_id):
        self._client.sadd(MESSAGE_ID_KEY.format(open_id),
                          message_id)
         


mc = McRedis(REDIS_URI) 
