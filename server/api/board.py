
from flask_restful import (reqparse, abort, Resource, fields, marshal)
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, fresh_jwt_required,
                                jwt_required, jwt_refresh_token_required)

from .. import db
from ..model import User, Board, BoardPost
from ..services.login import login_required, permission_required, get_user, UserPermission
from ..services.board import create_board, post_board, get_boards, get_posts, get_userinfo, post_post, BoardResult



MSG_REQUIRED = 'This field is required.'


class BoardManage(Resource):

    def get(self):
        boards = get_boards()
        result = []
        for b in boards:
            result.append({
                'id':b.id,
                'name':b.name,
                
            })
        
        return {"boards":result}, 200

    @permission_required(UserPermission.ADMIN)
    #@login_required
    #@jwt_required
    #@jwt_optional
    def post(self):
        
        parser = reqparse.RequestParser()

        parser.add_argument('name', type=str, required=True, help=MSG_REQUIRED)
        parser.add_argument('permission_read', type=int, default=0)
        parser.add_argument('permission_write', type=int, default=0)

        args = parser.parse_args()
        
        

        result = create_board(Board(name=args['name'], permission_read=args['permission_read'], 
                                permission_write=args['permission_write']),
                                get_user())
        

        return {}, 200


class UserField(fields.Raw):
    def format(self, value: User):
        return {
            'username':value.username, 
            'nickname':value.nickname
            }


post_field = {
    'title': fields.String,
    'content': fields.String,
    'vote_up': fields.Integer,
    'vote_down': fields.Integer,
    'visited': fields.Integer,
    'writer': UserField(attribute='owner')

}


class BoardPostList(Resource):

    
    def get(self, board_id):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('pagesize', type=int, default=10)

        args = parser.parse_args()

        args['pagesize'] = min(args['pagesize'], 50)

        result, posts = get_posts(board_id, amount=pagesize, start=page * pagesize)

        if result == BoardResult.NO_BOARD_EXISTS:
            return {"message":"게시판이 없습니다."}, 400

        output = [marshal(i, post_field) for i in posts]
        
        return {
            'count': len(output),
            'posts': output
        }, 200
    
    @login_required
    def post(self, board_id):
        parser = reqparse.RequestParser()


        parser.add_argument('title', type=str, required=True, help=MSG_REQUIRED)
        parser.add_argument('content', type=str, required=True, help=MSG_REQUIRED)
        
        args = parser.parse_args()

        newpost = BoardPost(title=args['title'], content=args['content'])
        result = post_post(board_id, newpost, get_user())
        if result == BoardResult.NO_BOARD_EXISTS:
            return {"message":"게시판이 없습니다."}, 400
        if result == BoardResult.SUCCESS:
            return {}, 201
        return {}, 500