from flask_restful import (reqparse, abort, Resource, fields, marshal)
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, fresh_jwt_required,
                                jwt_required, jwt_refresh_token_required)

from .. import db
from ..model import User, Board, BoardPost, Comment, BoardPostVote
from ..services.login import UserPermission, get_user, login_required, permission_required


user_field = {
    'username': fields.String,
    'nickname': fields.String,
    'email': fields.String
}


class UserField(fields.Raw):
    def format(self, value: User):
        return {
            'username':value.username, 
            'nickname':value.nickname
            }


class AdminManage(Resource):
    
    @permission_required(UserPermission.Admin)
    def get(self):
        admins = User.query.filter(1==1).all()
        
        return {
            'admins': [marshal(x, user_field) for x in admins]
        }, 200
        

class UserManageList(Resource):

    @permission_required(UserPermission.Admin)
    def get(self):
        users = User.query.all()

        return {
            "users": [marshal(x, user_field) for x in users]
        }, 200



class UserManage(Resource):

    @permission_required(UserPermission.Admin)
    def delete(self, username):
        user: User = User.query.filter_by(username=username).first()

        if user == None:
            return {}, 404

        db.session.delete(user)
        db.session.commit()

        return {}, 200
