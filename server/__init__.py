import os

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS

class VueFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='(%',
        block_end_string='%)',
        variable_start_string='((',
        variable_end_string='))',
        comment_start_string='(#',
        comment_end_string='#)',
    ))

STATIC_PATH = os.path.join(os.path.dirname(__file__), 'dists')

db = SQLAlchemy()

def create_app():
    app = VueFlask(__name__)

    app.config.from_json('../config.json')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    db.init_app(app)
    api = Api(app)
    
    jwt = JWTManager(app)

    CORS(app, resources={r'/*': {'origins': '*'}})

    with app.app_context():
        from . import routes
        from .api import load_api
        

        load_api(api, "/api/v1")

        return app