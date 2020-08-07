from flask import request, jsonify
from flask_restplus import Namespace, Resource

class AuthWxDto(object):
    ns = Namespace(name='auth_wx', description='微信认证接口')

ns = AuthWxDto.ns


@ns.route("")
class AuthWxApi(Resource):
    def get(self):
        pass
        return jsonify({"code": 0})
