from main.third_platform.wechat_platform import wechat_client
from main.third_platform.lingju import lingju_robot

def send_to_lingju(data, open_id):
    print(data)
    question = wechat_client.message_parse(data.get('msg', 'p'))
    msg_from_lingju = lingju_robot.parse_lingju(text=question)
    reply = wechat_client.reply_message(msg_from_lingju)
    return reply

