import sys
import json
import requests 
import traceback
from json.decoder import JSONDecodeError
import asyncio
import aiohttp

sys.path.insert(0, '../..')

from main.store.mcredis import mc
from main.utils.common import logger

LingJu_USERID = '2bcc17cc0d4c49cd99026fc4af9d331a'    # 用户id uuid生成
# CJ个人
LingJu_APPKEY = '0bcf3d5c2fdcfe7577beb0ca0a5c528b'    # 灵聚APPKEY
LingJu_AUTHCODE = '9faae0387fd3a8915dddd0cfb9326631'  # 灵聚授权码
# 公司
# LingJu_APPKEY = '8bed9fdbbaabd112b62bdc7e9a54d38e'
# LingJu_AUTHCODE = '9149758ec78b28872c1eab5981258b89'


class ParseLingJuMixin(object):
    # API调用地址
    API_URL = 'https://dev.lingju.ai/httpapi'
    # redis存储accessToken的key
    ACCESS_TOKEN_KEY = 'LingJu:accessToken'
    # 灵聚错误码映射关系
    LINGJU_CODE_MAP = {
        '0': '成功', '-1': '系统异常', '1': '其它错误', '4': '开发者帐号错误，账户未完成认证或已被禁用',
        '6': 'APPKEY无效', '7': 'model错误', '8': '参数错误', '9': '已经是最新版本', '10': '重复操作',
        '11': '授权码无效', '12': '激活码重置过于频繁', '13': '体验版授权码已过期', '14': '激活失败，请重试',
        '15': '连接中禁止切换用户', '16': '终端未激活', '17': '激活码已过期，请重置', '18': '激活码无效',
        '19': '会话过期', '20': '数据格式校验错误', '98': '重复登录', '99': '未登录', '111': '参数错误',
        '21': '数据格式校验错误', '22': '数据格式校验错误', '23': '数据格式校验错误', '24': '数据格式校验错误',
        '25': '数据格式校验错误', '26': '数据格式校验错误', '27': '数据格式校验错误', '28': '数据格式校验错误',
        '29': '数据格式校验错误', '40': '并发过高导致请求失败', '41': '每次调用次数已达上限', '97': '校验失败',
        '42': '目标对象未同步，请先通过update接口更新后重试', '43': '应用无效，已被限制使用', '44': '应用无效，已废弃',
        '45': '目标对象数量已达上限', '114': '帐号未认证', '120': '账号已被禁用', '121': '授权限额已满',
        '122': 'accessToken已过期', '123': '没有调用http接口的权限', '124': '系统应答超时', '129': '应用已被限制'
    }

    def __init__(self):
        """
        实例化对象时判断accessToken是否可用
        """
        # super(ParseLingJuMixin, self).__init__()
        self.token = mc.get(self.ACCESS_TOKEN_KEY)
        # print("redis 中 token为：{}".format(self.token))
        logger.info("redis 中 token为：{}".format(self.token))
        if not self.token:
            # 重新获取accessToken
            res = requests.get(url="{}/{}".format(self.API_URL, 'authorize.do'),
                               params={'appkey': LingJu_APPKEY, 'userid': LingJu_USERID, 'authcode': LingJu_AUTHCODE})

            # with aiohttp.ClientSession() as client:
            #     res = await client.get(url="{}/{}".format(self.API_URL, 'authorize.do'),
            #                            params={'appkey': LingJu_APPKEY, 'userid': LingJu_USERID, 'authcode': LingJu_AUTHCODE})

            try:
                result = res.json()
                logger.info("请求accessToekn返回：{}".format(result))
                self.token = result['data']['accessToken']
                expires = int(result['data']['expires']) - 1
                mc.set(name=self.ACCESS_TOKEN_KEY, value=self.token, ex=expires*3600)
            except Exception as e:
                logger.info("获取灵聚机器人accesToken出错： {}".format(e))
                raise

    async def get_lingju(self, text='', uid='', loc='', post=None):
        """
        请求灵聚机器人
        """
        post_data = {
            "accessToken": self.token,
            "input": text,
            "city": loc,
        }

        try:
            logger.info("调用灵聚机器人api")

            try:
                # res = await trequests.post(url='{}/{}'.format(self.API_URL, 'ljchat.do'),
                #                            headers={'Content-Type': 'application/json;charset=UTF-8'},
                #                            json=post_data, timeout=10)
                print(type(post_data))
                async with aiohttp.ClientSession() as client:
                    res = await client.post(url='{}/{}'.format(self.API_URL, 'ljchat.do'),
                                            headers={'Content-Type': 'application/json;charset=UTF-8'},
                                            json=post_data, timeout=10)
            except Exception as e:
                logger.info("访问灵聚机器人出错 {}".format(str(e)))
                logger.info(traceback.format_exc())
                return 408, 'error', '超时'

            result = res.json()
            logger.info("状态码： {}， 状态： {}， 结果： {}".format(res.status, '', result))
            return res.status, '', result
        except Exception as e:
            logger.info("调用灵聚机器人api出错： {}".format(e))
            logger.info(traceback.format_exc())
            return 404, 'error', '调用灵聚机器人api出错'

    async def parse_lingju(self, text='', uid='', loc='', post=None):
        """
        对灵聚机器人的返回结果进行解析, 返回一个文本答案
        """
        status, reason, result = await self.get_lingju(text=text, uid=uid, loc=loc, post=post)
        if status == 200:
            result = await result
            code = result.get('status')
            logger.info("请求灵聚机器人结果：{}".format(self.LINGJU_CODE_MAP[str(code)]))
            if code == 0:
                try:
                    answer = json.loads(result['answer'])
                    logger.info("灵聚机器人返回结果为带指令的回复")
                    answer = answer.get('rtext', '暂不知道该功能')

                except JSONDecodeError as to_json_error:
                    # 无法解析为json 返回的是纯文本
                    logger.info("灵聚机器人返回结果为普通文本")
                    answer = result['answer']

                except Exception as e:
                    logger.error("灵聚机器人返回结果解析错误：{}".format(e))
                    logger.info(traceback.format_exc())
                    answer = ''

            else:
                answer = ''

        else:
            logger.info("获取灵聚机器人数据出错")
            answer = ''

        # print("解析结果：{}".format(answer))
        logger.info("解析结果：{}".format(answer))
        return answer


parse_lingju = ParseLingJuMixin()


if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(parse_lingju.get_lingju(text="你是谁？"))
    loop.run_until_complete(parse_lingju.parse_lingju(text="别生气"))
