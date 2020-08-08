from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply

from main.store.mcredis import mc

class WeChatCliet(object):
    def __init__(self, reids):
        self.mc = redis
        pass

    def message_parse(self, xml_message):
        """消息解析"""
        message = prase_message(xml_message)
        return message

    def message_distinct(self, message):
        """消息重复校验
        重复：True
        不重复: False
        """
        if not message.id:
            return True

        if self.mc._messgae_repeat(message):
            logger.warning("拦截消息:\n msg: {}\n".format(message))
            return False

        else:
            self.mc._save_message(message.id):
            return True

    def reply_message(self, to_open_message, msg):
        """
        :param to_open_messgae 要回复给访客的消息
        :param msg 收到的消息解析后保存在msg
        """
        reply = TextReply(content=to_open_message, message=msg)
        # 转换成 XML
        xml = reply.render()
        return xml


wechat_client = WeChatClient(mc)
