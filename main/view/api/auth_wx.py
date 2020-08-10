from flask import request, jsonify
from flask_restplus import Namespace, Resource

from main.service.api.auth_wx import check_wx_offical
from main.service.api.message_wx import send_to_lingju 

class AuthWxDto(object):
    ns = Namespace(name='auth_wx', description='微信认证接口')

ns = AuthWxDto.ns


@ns.route("")
class AuthWxApi(Resource):
    def get(self):
        print("收到wx认证请求")
        return check_wx_offical(request.args)


    def post(self):
        print("收到wx推送消息")
        print(request.json)
        print(request.args)
        return send_to_lingju(request.json)
