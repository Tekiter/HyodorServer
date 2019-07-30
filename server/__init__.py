from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_json('../config.json')

    db.init_app(app)
    api = Api(app)
    
    jwt = JWTManager(app)

    CORS(app, resources={r'/*': {'origins': '*'}})

    with app.app_context():
        from . import routes
        from .api import load_api
        

        load_api(api, "/api/v1")

        return app