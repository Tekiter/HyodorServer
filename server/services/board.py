import functools

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from .. import db
from ..model import User, Board, BoardPost, Comment, BoardPostVote
from .login import login_required, get_userinfo, get_user, UserPermission

from typing import List




class BoardResult:
    SUCCESS = 0
    INTERNAL_ERROR = 4
    DB_ERROR = 5
    EXISTS = 10
    
    NOT_EXISTS = 11
    NOT_OWNER = 12
    NO_BOARD_EXISTS = 20
    PERMISSION_REQUIRED = 40



def create_board(board: Board, owner: User):
    board.owner = owner
    try:
        db.session.add(board)
        db.session.commit()

        return BoardResult.SUCCESS
    except IntegrityError:
        db.session.rollback()
        return BoardResult.EXISTS
    except:
        return BoardResult.DB_ERROR
    pass

def delete_board(board_id):
    user = get_user()

    board: Board = Board.query.get(board_id)

    if board == None:
        return BoardResult.NOT_EXISTS

    if user.permission == UserPermission.Admin:
        db.session.delete(board)
        db.session.commit()
        try:
            pass
        except:
            return BoardResult.DB_ERROR

        return BoardResult.SUCCESS

    return BoardResult.PERMISSION_REQUIRED



def post_board(board_id, post: BoardPost, owner: User):
    board: Board = Board.query.filter_by(id=board_id).first()
    
    
    if board == None:
        return BoardResult.NO_BOARD_EXISTS

    board.owner = owner
    try:
    
        board.posts.append(post)

        db.session.commit()
    except:
        return BoardResult.DB_ERROR

    return BoardResult.SUCCESS


def get_boards() -> List[Board]:
    result = []

    boards = Board.query.all()

    for b in boards:
        result.append(b)

    return result


def get_post_count(board_id):
    return BoardPost.query.filter_by(board_id=board_id).count()


def get_posts(board_id=None, amount=None, start=0) -> List[BoardPost]:
    result : List[BoardPost] = []

    targetboard: Board = Board.query.filter_by(id=board_id).first()
    if targetboard == None:
        return BoardResult.NO_BOARD_EXISTS, None

    posts = BoardPost.query.filter_by(board_id=board_id).order_by(BoardPost.id.desc())
    if amount != None:
        posts = posts.limit(amount)
        if start != None and start >= 0:
            posts = posts.offset(start)
    

    for p in posts:
        result.append(p)
    
    return BoardResult.SUCCESS, result


def post_post(board_id, post: BoardPost, owner: User) -> BoardResult:
    board: Board = Board.query.filter_by(id=board_id).first()


    if board == None:
        return BoardResult.NO_BOARD_EXISTS

    post.owner = owner
    post.board = board

    board.posts.append(post)
    try:
        db.session.commit()
    except:
        return BoardResult.DB_ERROR

    return BoardResult.SUCCESS


def delete_post(post_id):
    post: BoardPost = BoardPost.query.get(post_id)

    if post == None:
        return BoardResult.NOT_EXISTS


    user = get_user()


    if post.owner != user and user.permission < UserPermission.Admin:
        return BoardResult.NOT_OWNER

    db.session.delete(post)
    try:
        db.session.commit()
    except:
        return BoardResult.DB_ERROR
    return BoardResult.SUCCESS


def edit_post(post_id, epost: BoardPost) -> BoardResult:
    opost: BoardPost = BoardPost.query.get(post_id)



    if opost == None:
        return BoardResult.NOT_EXISTS

    user = get_user()

    if opost.owner != user and user.permission < UserPermission.Admin:
        return BoardResult.NOT_OWNER

    opost.title = epost.title
    opost.content = epost.content
        
    
    try:
        db.session.commit()
    except:
        return BoardResult.DB_ERROR

    return BoardResult.SUCCESS

    


def get_post_content(post_id):
    post: BoardPost = BoardPost.query.filter_by(id=post_id).first()
    
    if post == None:
        return BoardResult.NOT_EXISTS, None
    return BoardResult.SUCCESS, post


def vote_up_post(post_id):
    user = get_user()
    
    vote = BoardPostVote.query.filter(BoardPostVote.post_id==post_id, BoardPostVote.owner_id==user.id, BoardPostVote.is_comment==False).first()
    if vote == None:
        BoardPostVote(post_id=post_id, owner_id=user.id, vote_up=1)
        return BoardResult.SUCCESS
    else:
        if vote.vote_up == 0:
            vote.vote_up = 1
            vote.vote_down = 0

            db.session.commit()
            return BoardResult.SUCCESS
    return BoardResult.EXISTS

def vote_down_post(post_id):
    user = get_user()
    
    vote = BoardPostVote.query.filter(BoardPostVote.post_id==post_id, BoardPostVote.owner_id==user.id, BoardPostVote.is_comment==False).first()
    if vote == None:
        BoardPostVote(post_id=post_id, owner_id=user.id, vote_down=1)
        return BoardResult.SUCCESS
    else:
        if vote.vote_down == 0:
            vote.vote_down = 1
            vote.vote_up = 0

            db.session.commit()
            return BoardResult.SUCCESS
    return BoardResult.EXISTS



def post_comment(post_id, comment: Comment, owner: User, parent_id = None):
    result, post = get_post_content(post_id)
    if result == BoardResult.SUCCESS:
        comment.owner = owner
        comment.post = post
        if parent_id != None:
            
            comment.parent_id = parent_id

        post.comments.append(comment)
        try:
            db.session.commit()
        except:
            return BoardResult.DB_ERROR

        return BoardResult.SUCCESS
    return BoardResult.NOT_EXISTS


def get_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if comment == None:
        return BoardResult.NOT_EXISTS, None
    
    return BoardResult.SUCCESS, comment


def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)

    if comment == None:
        return BoardResult.NOT_EXISTS

    user = get_user()

    if comment.owner != user and user.permission < UserPermission.Admin:
        return BoardResult.NOT_OWNER

    db.session.delete(comment)
    try:
        db.session.commit()
    except:
        return BoardResult.DB_ERROR
    return BoardResult.SUCCESS
    
def edit_comment(comment_id, ecmt: Comment) -> BoardResult:
    ocmt: Comment = Comment.query.get(comment_id)

    if ocmt == None:
        return BoardResult.NOT_EXISTS

    user = get_user()
    if ocmt.owner != user and user.permission < UserPermission.Admin:
        return BoardResult.NOT_OWNER

    ocmt.content = ecmt.content
    
    try:
        db.session.commit()
    except:
        return BoardResult.DB_ERROR

    return BoardResult.SUCCESS
