import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .util import enc



class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
    permission = db.Column(db.Integer, default=0)
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if kwargs.get('password') != None:
            self.password = self.encrypt_password(kwargs['password'])

    def encrypt_password(self, password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)
    

class UserAddi(db.Model):
    __tablename__ = "UserAddi"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    user = db.relationship(User.__tablename__, backref=db.backref("moreinfo", lazy=True, cascade="all, delete-orphan"))


    age = db.Column(db.Integer)
    regidence = db.Column(db.String(100))
    lastcheck = db.Column(db.DateTime)
    hobby = db.Column(db.String(100))
    mediinfo = db.Column(db.String(1000))


class ParentInfo(db.Model):
    __tablename__ = "ParentInfo"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=True)
    user = db.relationship(User.__tablename__, backref=db.backref("parentinfos", lazy=True, cascade="all, delete-orphan"))

    relation = db.Column(db.String(1000), nullable=False)
    name = db.Column(db.String(1000))
    gender = db.Column(db.String(1000))
    birthday = db.Column(db.String(1000))

    last_checkup = db.Column(db.String(1000))

    prefer_call = db.Column(db.Integer)
    prefer_visit = db.Column(db.Integer)

    additional_info = db.Column(db.String(5000))

    def get_column(self, column_name):
        return enc.decrypt(getattr(self, column_name))

    def set_column(self, column_name, value):
        setattr(self, column_name, enc.encrypt(value))

    def get_enc_datetime(self, column_name) -> dt.datetime:
        timestamp = self.get_column(column_name)
        return dt.datetime.fromtimestamp(timestamp)

    def set_enc_datetime(self, column_name, value: dt.datetime):
        self.set_column(self, column_name, value.timestamp())



class Schedule(db.Model):
    __tablename__ = "Schedule"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    owner = db.relationship(User.__tablename__, backref=db.backref("schedules", lazy=True))

    type = db.Column(db.Integer, default=0)
    content = db.Column(db.String())
    datetime = db.Column(db.DateTime)



class Board(db.Model):
    __tablename__ = "Board"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    permission_read = db.Column(db.Integer, nullable=False, default=0)
    permission_write = db.Column(db.Integer, nullable=False, default=0)


    owner_id = db.Column(db.Integer, db.ForeignKey(User.__tablename__+".id"))

    owner = db.relationship(User.__tablename__, backref=db.backref("boards", lazy=True))


class BoardPost(db.Model):
    __tablename__ = "BoardPost"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(2000), nullable=False)

    vote_up = db.Column(db.Integer, default=0)
    vote_down = db.Column(db.Integer, default=0)
    visited = db.Column(db.Integer, default=0)  

    owner_id = db.Column(db.Integer, db.ForeignKey(User.__tablename__+".id"))
    board_id = db.Column(db.Integer, db.ForeignKey(Board.__tablename__+".id"))

    owner = db.relationship(User.__tablename__, backref=db.backref("posts"))
    board = db.relationship(Board.__tablename__, backref=db.backref("posts", lazy=True, cascade="all, delete-orphan"))


class BoardPostVote(db.Model):
    __tablename__ = "BoardPostVote"

    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey(BoardPost.__tablename__+".id"))
    owner_id = db.Column(db.Integer, db.ForeignKey(User.__tablename__+".id"))

    
    is_comment = db.Column(db.Boolean, default=False)
    
    vote_up = db.Column(db.Integer, default=0)
    vote_down = db.Column(db.Integer, default=0)

    post = db.relationship(BoardPost.__tablename__, backref=db.backref("votes", lazy=True, cascade="all, delete-orphan"))
    owner = db.relationship(User.__tablename__)



class Comment(db.Model):
    __tablename__ = "Comment"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)

    vote_up = db.Column(db.Integer, default=0)
    vote_down = db.Column(db.Integer, default=0)   

    parent_id = db.Column(db.Integer, db.ForeignKey(__tablename__+".id"))
    owner_id = db.Column(db.Integer, db.ForeignKey(User.__tablename__+".id"))
    post_id = db.Column(db.Integer, db.ForeignKey(BoardPost.__tablename__+".id"))
    

    parent = db.relationship(__tablename__, backref=db.backref("children", remote_side=[id]))
    owner = db.relationship(User.__tablename__, backref=db.backref("comments", lazy=True))
    post = db.relationship(BoardPost.__tablename__, backref=db.backref("comments", lazy=True, cascade="all, delete-orphan"))




