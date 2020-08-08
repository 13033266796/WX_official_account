from flask import Blueprint
from flask_restplus import Api

from main.view.api.auth_wx import ns as auth_wx_ns
from main.view.api.wx_message import ns as message_wx_ns


def test():
    pass

def register_api(app):
    blueprint = Blueprint(name='api', import_name=__name__, url_prefix="/api/v1")
    api = Api(
            app=blueprint,
            version='1.0',
            title='New Api',
          )
    api.add_namespace(auth_wx_ns, path="/wx")
    api.add_namespace(message_wx_ns, path="/callback")


    blueprint.before_request(test)
    
    app.register_blueprint(blueprint)
