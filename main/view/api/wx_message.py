from flask import request, jsonify
from flask_restplus import Namespace, Resource

from main.service.api.auth_wx import check_wx_offical

class MessageWxDto(object):
    ns = Namespace(name='message_wx', description='微信认证接口')

ns = AuthWxDto.ns


@ns.route("/callback/<open_id>")
class MessageWxApi(Resource):
    def post(self, open_id):
        return check_wx_offical(request.json, open_id)
