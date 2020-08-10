from flask import jsonify, Response
import hashlib

TOKEN = '15297840370'


def check_wx_offical(data):
    signature = data.get('signature')
    timestamp = data.get('timestamp')
    nonce = data.get('nonce')
    echostr = data.get('echostr')

    sha1_ = [TOKEN, timestamp, nonce]
    sha1_ = sorted(sha1_)
    sha1_ = "".join(sha1_)

    sha1_ = hashlib.sha1(sha1_.encode('utf-8'))
    sha1_ = sha1_.hexdigest()
    if sha1_ == signature:
        return Response(echostr, status=200, mimetype="application/json")
 
    return None

