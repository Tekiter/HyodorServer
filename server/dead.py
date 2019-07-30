import sys
sys.path.insert(0, "../")


from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, jwt_required, create_access_token, get_jwt_identity)
from flask_restful import (reqparse, abort, Api, Resource)
from flask_sqlalchemy import SQLAlchemy


#from model.database import db
from api import load_api


DEBUG = True

app = Flask(__name__)

app.config.from_object(__name__)
app.config['JWT_SECRET_KEY'] = 'secret-key-ha'
app.config['SECRET_KEY'] = 'secret-key-second'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://cert:roqkfqhdks@203.229.206.16:12344/cert'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


api = Api(app)
jwt = JWTManager(app)
db.init_app(app)

CORS(app, resources={r'/*': {'origins': '*'}})



@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')



@app.route("/authtest")
@jwt_required
def authtest():
    iden = get_jwt_identity()
    return str(iden)
    

load_api(api, "/api/v1")



if __name__ == '__main__':
    app.run()

    
