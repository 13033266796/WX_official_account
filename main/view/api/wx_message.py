from flask import request, jsonify
from flask_restplus import Namespace, Resource

from main.service.api.auth_wx import check_wx_offical

class MessageWxDto(object):
    ns = Namespace(name='message_wx', description='微信认证接口')

ns = MessageWxDto.ns


@ns.route("/pong")
class PongApi(Resource):
    def get(self):
        return jsonify({"code": 0})

@ns.route("/callback/<open_id>")
class MessageWxApi(Resource):
    def post(self, open_id):
        return send_message_to_lingju(request.json, open_id)
