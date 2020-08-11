from flask import Response

from main.third_platform.wechat_platform import wechat_client
from main.third_platform.lingju import lingju_robot

def send_to_lingju(data):
    xml = str(data, encoding='utf-8')
    print("************************")
    print(xml)
    
    request_data = wechat_client.message_parse(xml)
    print("-------------------------------")
    print(request_data)

    msgType = request_data.type
    open_id = request_data.source
    target = request_data.target
    content = request_data.content
    if msgType == 'text':
        msg_from_lingju = lingju_robot.parse_lingju(text=content)
        reply = wechat_client.reply_message(open_id, target, msg_from_lingju, request_data)
        print(reply)
        # return reply
        return Response(reply, status=200, mimetype="application/json")
    else:
        return '暂不支持除文字以外的消息哦'

