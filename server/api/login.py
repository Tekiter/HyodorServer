
from flask_restful import (reqparse, abort, Resource)
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, fresh_jwt_required,
                                jwt_required, jwt_refresh_token_required)
import re
import datetime

from ..model import User
from .. import db
from ..services.login import login_required, login, register, create_login_token, withdraw, LoginResult


MSG_REQUIRED = 'This field is required.'



def valid_username(username):
    if re.match("^([a-z0-9]){6,}$", username):
        return True
    return False

def valid_password(password):
    if re.match("^[A-Za-z0-9~`!@#$%\^&*()-+=]{6,30}$", password):
        return True
    return False

def valid_email(email):
    if re.match("^[A-Za-z0-9]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[A-Za-z0-9])*\.[A-Za-z]{2,3}$", email):
        return True
    return False

def valid_nickname(nickname):
    if re.match("^([가-힣A-Za-z0-9]|_|-){2,}$", nickname):
        return True
    return False



class Login(Resource):

    @login_required
    def get(self):
        
        iden = get_jwt_identity()
        
        return iden


    # login
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help=MSG_REQUIRED)
        parser.add_argument('password', type=str, required=True, help=MSG_REQUIRED)

        
        
        args = parser.parse_args()
        

        result, user = login(args['username'], args['password'])
        if result == LoginResult.SUCCESS:
            
            access_token, refresh_token = create_login_token(user)
        
            json = {
                'username': str(user.username),
                'nickname': str(user.nickname),
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }
            return json, 200

        return {"msg": "올바르지 않은 아이디 또는 비밀번호입니다."}, 401


    # register
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help=MSG_REQUIRED)
        parser.add_argument('password', type=str, required=True, help=MSG_REQUIRED)
        parser.add_argument('email', type=str, required=True, help=MSG_REQUIRED)
        parser.add_argument('nickname', type=str, required=True, help=MSG_REQUIRED)

        args = parser.parse_args()

        errors = {}

        if not valid_username(args['username']):
            errors["username"] = "아이디는 6자리 이상의 영문자 또는 숫자여야 합니다."
        
        if not valid_password(args['password']):
            errors["password"] = "비밀번호는 6자리 이상이어야 합니다."

        if not valid_email(args['email']):
            errors["email"] = "올바르지 않은 이메일 형식입니다."
        
        if not valid_nickname(args['nickname']):
            errors["nickname"] = "올바르지 않은 닉네임 형식입니다."

        if len(errors) != 0:
            return errors, 400

        



        newuser = User(username=args['username'], email=args['email'], 
                        password=args['password'], nickname=args['nickname'],
                        created=datetime.datetime.now())

        result = register(newuser)

        if result == LoginResult.SUCCESS:
            return {"username":newuser.username}, 201
        elif result == LoginResult.EMAIL_EXISTS:
            return {"email":"이미 사용중인 이메일입니다."}, 409
        elif result == LoginResult.USERNAME_EXISTS:
            return {"username":"이미 사용중인 아이디입니다."}, 409
        elif result == LoginResult.USER_EXISTS:
            return {"email":"이미 사용중인 이메일입니다.",
                    "username":"이미 사용중인 아이디입니다."}, 409
        else:
            return {"msg":"알 수 없는 오류입니다."}, 500

    
    def delete(self):
        parser = reqparse.RequestParser()

        parser.add_argument("")


class LoginRefresh(Resource):

    @jwt_refresh_token_required
    def get(self):
        cur = get_jwt_identity()
        new_access = create_access_token(identity=cur, fresh=False)
        return {'access_token': new_access}, 200


class LoginDebug(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help=MSG_REQUIRED)
        parser.add_argument('password', type=str, required=True, help=MSG_REQUIRED)

        
        
        args = parser.parse_args()
        

        result, user = login(args['username'], args['password'])
        if result == LoginResult.SUCCESS:
            
            access_token, refresh_token = create_login_token(user, expires_delta=datetime.timedelta(days=30))
        
            json = {
                'is_debug': True,
                'username': str(user.username),
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            }
            return json, 200

        return {"msg": "올바르지 않은 아이디 또는 비밀번호입니다."}, 400

    