from flask import request, jsonify
from flask_restplus import Namespace, Resource

from main.service.api.auth_wx import check_wx_offical

class AuthWxDto(object):
    ns = Namespace(name='auth_wx', description='微信认证接口')

ns = AuthWxDto.ns


@ns.route("")
class AuthWxApi(Resource):
    def get(self):
        return check_wx_offical(request.args)
