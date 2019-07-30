import functools

from sqlalchemy.exc import IntegrityError

from .. import db
from ..model import User, Board, BoardPost, Comment
from .login import login_required, get_userinfo, get_user

from typing import List




class BoardResult:
    SUCCESS = 0
    INTERNAL_ERROR = 4
    DB_ERROR = 5
    BOARDNAME_EXISTS = 10
    NOT_EXISTS = 11
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
        return BoardResult.BOARDNAME_EXISTS
    except:
        return BoardResult.DB_ERROR
    pass


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


def get_posts(board_id=None, amount=None, start=0) -> List[BoardPost]:
    result : List[BoardPost] = []

    targetboard: Board = Board.query.filter_by(id=board_id).first()
    if targetboard == None:
        return BoardResult.NO_BOARD_EXISTS, None

    # posts = BoardPost.query.filter_by(id=board_id).offset(start)
    posts = BoardPost.query.filter_by(board_id=board_id).order_by(BoardPost.id.desc())
    if amount != None:
        posts = posts.limit(amount)
        if start != None:
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
