import functools

from flask import abort, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, create_refresh_token
from sqlalchemy.exc import IntegrityError

from .. import db
from ..model import User


class LoginResult:
    SUCCESS = 0
    INVALID_IDPW = 10
    USER_EXISTS = 20
    USERNAME_EXISTS = 21
    EMAIL_EXISTS = 22

    INTERNAL_ERROR = 30


class UserPermission:
    Guest = 0
    BasicUser = 1
    Admin = 0xfefefe
    WEB_MASTER = 0xffffff




def login(username, password):
    cur : User = User.query.filter_by(username=username).first()
    
    if cur != None and cur.verify_password(password):
        return LoginResult.SUCCESS, cur
    return LoginResult.INVALID_IDPW, None


def create_login_token(user: User, **kwargs):
    iden = {
        'type': 'login',
        'username': user.username,
        'nickname': user.nickname,
        'perm': user.permission
    }
    return create_access_token(iden, **kwargs), create_refresh_token(iden, **kwargs)


def register(newuser: User):
    if field_exists(User.username, newuser.username):
        return LoginResult.USERNAME_EXISTS
    if field_exists(User.email, newuser.email):
        return LoginResult.EMAIL_EXISTS
    


    try:
        db.session.add(newuser)
        db.session.commit()

        return LoginResult.SUCCESS
    except IntegrityError:
        db.session.rollback()
        return LoginResult.USER_EXISTS
    except:
        return LoginResult.INTERNAL_ERROR


def field_exists(field, value):
    user = User.query.filter(field == value).first()
    return user != None
    

def get_userinfo():
    iden = get_jwt_identity()
    return iden

def get_user() -> User:
    userinfo = get_userinfo()
    if userinfo == None:
        raise Exception("Not logged in")

    user = User.query.filter_by(username=userinfo['username']).first()
    return user

def get_user_permission():
    iden = get_jwt_identity()
    if iden == None:
        return -1
    return iden["perm"]


def login_required(func):
    @functools.wraps(func)
    @jwt_required
    def wrapper(*args, **kwargs):
        iden = get_jwt_identity()
        
        if iden == None or iden.get('type') != 'login':
            return {'msg':'로그인이 필요합니다.'}, 401
        return func(*args, **kwargs)
    return wrapper


def permission_required(min_level):
    def deco(func):
        @functools.wraps(func)
        @login_required
        def wrapper(*args, **kwargs):
            iden = get_jwt_identity()
            
            if iden.get('perm', 0) >= min_level:
                return func(*args, **kwargs)
            return {'msg':'권한이 부족합니다.'},403
        return wrapper
    return deco


