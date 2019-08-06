
from flask_restful import (reqparse, abort, Resource, fields, marshal)
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt_identity, fresh_jwt_required,
                                jwt_required, jwt_refresh_token_required)

from .. import db
from ..model import User, Board, BoardPost, Comment, BoardPostVote
from ..services.login import login_required, permission_required, get_user, UserPermission
from ..services.board import (create_board, post_board, get_boards, get_posts, get_userinfo, post_post, BoardResult,
                            get_post_count, get_post_content, post_comment, delete_post, delete_comment, get_comment)



MSG_REQUIRED = 'This field is required.'



class UserField(fields.Raw):
    def format(self, value: User):
        return {
            'username':value.username, 
            'nickname':value.nickname
            }


post_field = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'vote_up': fields.Integer,
    'vote_down': fields.Integer,
    'visited': fields.Integer,
    'writer': UserField(attribute='owner')

}

class CommentField(fields.Raw):
    def format(self, value: Comment):
        return {
            'id': value.id,
            'content': value.content,
            'vote_up': value.vote_up,
            'vote_down': value.vote_down,
            'writer': UserField().format(value.owner)
        }


post_content_field = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'vote_up': fields.Integer,
    'vote_down': fields.Integer,
    'visited': fields.Integer,
    'writer': UserField(attribute='owner'),
    'comments': fields.List(CommentField)

}




class BoardManage(Resource):

    def get(self):
        boards = get_boards()
        result = []
        for b in boards:
            result.append({
                'id':b.id,
                'name':b.name,
                'count':get_post_count(b.id)
            })
        
        return {"boards":result}, 200

    @permission_required(UserPermission.Guest)
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





class BoardPostList(Resource):

    
    def get(self, board_id):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('pagesize', type=int, default=10)

        args = parser.parse_args()

        args['pagesize'] = min(args['pagesize'], 50)

        result, posts = get_posts(board_id, amount=args['pagesize'], start=(args['page'] - 1) * args['pagesize'])

        if result == BoardResult.NO_BOARD_EXISTS:
            return {"message":"게시판이 없습니다."}, 400

        output = [marshal(i, post_field) for i in posts]
        
        return {
            'totalcount': get_post_count(board_id),
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
            return {"message":"게시판이 없습니다."}, 404
        if result == BoardResult.SUCCESS:
            return {}, 201
        return {}, 500






class BoardPostView(Resource):

    def get(self, post_id):
        
        result, post = get_post_content(post_id)
        if result == BoardResult.SUCCESS:

            return marshal(post, post_content_field), 200
        if result == BoardResult.NOT_EXISTS:
            return {"message":"게시글이 없습니다."}, 404

        return {}, 500

    @login_required
    def delete(self, post_id):

        result = delete_post(post_id)

        if result == BoardResult.NOT_EXISTS:
            return {"message":"게시글이 없습니다."}, 404
        if result == BoardResult.NOT_OWNER:
            return {"message":"권한이 없습니다."}, 403

        if result == BoardResult.SUCCESS:
            return {}, 200
        

        return {}, 500


class BoardComment(Resource):

    @login_required
    def post(self):

        parser = reqparse.RequestParser()

        
        parser.add_argument('post_id', type=int, required=True, help=MSG_REQUIRED)
        parser.add_argument('content', type=str, required=True, help=MSG_REQUIRED)

        args = parser.parse_args()
        post_id = args['post_id']
        content = args['content']

        comment = Comment(content=content)

        result = post_comment(post_id, comment, get_user())

        if result == BoardResult.SUCCESS:
            return {}, 201
        if result == BoardResult.NOT_EXISTS:
            return {"message":"게시글이 없습니다."}, 404
        return {}, 500


class BoardCommentAction(Resource):

    def get(self, comment_id):
        result, comment = get_comment(comment_id)

        if result == BoardResult.SUCCESS:
            return CommentField().format(comment), 200
        if result == BoardResult.NOT_EXISTS:
            return {"message":"덧글이 없습니다."}, 404
        return {}, 500

    @login_required
    def delete(self, comment_id):
        result = delete_comment(comment_id)

        if result == BoardResult.SUCCESS:
            return {}, 200
        if result == BoardResult.NOT_EXISTS:
            return {"message":"덧글이 없습니다."}, 404
        if result == BoardResult.NOT_OWNER:
            return {"message":"권한이 없습니다."}, 403
        return {}, 500