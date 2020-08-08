from flask import jsonify
TOKEN = 'XXXXXXXX'


def check_wx_offical(data):
    signature = data.get('signature')
    timestamp = data.get('timestamp')
    nonce = data.get('nonce')
    echostr = data.get('echostr')

    sha1_ = [TOKEN, timestamp, nonce]
    sha1_ = sorted(sha1_)
    sha1_ = "".join(sha1_)

    if sha1_ == signature:
        return jsonify({'echostr': echostr})
    
    return None

