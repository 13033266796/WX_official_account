from flask import Flask
from flask_restplus import Api

from main.view.api import register_api

api = Api()

def create_app(name=None, _config=None):
    app = Flask(name)
    
    api.init_app(app)

    register_api(app)

    return app


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)
