from werkzeug.security import generate_password_hash, check_password_hash

from . import db



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
    user = db.relationship(User.__tablename__, backref=db.backref("moreinfo", lazy=True))


    age = db.Column(db.Integer)
    regidence = db.Column(db.String(100))
    lastcheck = db.Column(db.DateTime)
    hobby = db.Column(db.String(100))
    mediinfo = db.Column(db.String(1000))


class ParentInfo(db.Model):
    __tablename__ = "ParentInfo"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    user = db.relationship(User.__tablename__, backref=db.backref("parentinfos", lazy=True))

    relation = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    birthday = db.Column(db.DateTime)

    prefer_call = db.Column(db.Integer)
    prefer_visit = db.Column(db.Integer)


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


    owner_id = db.Column(db.Integer, db.ForeignKey(User.__tablename__+".id"), nullable=False)

    owner = db.relationship(User.__tablename__, backref=db.backref("boards", lazy=True))


class BoardPost(db.Model):
    __tablename__ = "BoardPost"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(2000), nullable=False)

    vote_up = db.Column(db.Integer, default=0)
    vote_down = db.Column(db.Integer, default=0)
    visited = db.Column(db.Integer, default=0)  

    owner_id = db.Column(db.Integer, db.ForeignKey(User.__tablename__+".id"), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey(Board.__tablename__+".id"), nullable=False)

    owner = db.relationship(User.__tablename__, backref=db.backref("posts"))
    board = db.relationship(Board.__tablename__, backref=db.backref("posts", lazy=True))


class BoardPostVote(db.Model):
    __tablename__ = "BoardPostVote"

    id = db.Column(db.Integer, primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey(BoardPost.__tablename__+".id"), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey(User.__tablename__+".id"), nullable=False)

    
    is_comment = db.Column(db.Boolean, default=False)
    
    vote_up = db.Column(db.Integer, default=0)
    vote_down = db.Column(db.Integer, default=0)

    post = db.relationship(BoardPost.__tablename__, backref=db.backref("votes", lazy=True, cascade="delete"))
    owner = db.relationship(User.__tablename__)



class Comment(db.Model):
    __tablename__ = "Comment"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)

    vote_up = db.Column(db.Integer, default=0)
    vote_down = db.Column(db.Integer, default=0)   

    parent_id = db.Column(db.Integer, db.ForeignKey(__tablename__+".id"))
    owner_id = db.Column(db.Integer, db.ForeignKey(User.__tablename__+".id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(BoardPost.__tablename__+".id"), nullable=False)
    

    parent = db.relationship(__tablename__, backref=db.backref("children", remote_side=[id]))
    owner = db.relationship(User.__tablename__, backref=db.backref("comments", lazy=True))
    post = db.relationship(BoardPost.__tablename__, backref=db.backref("comments", lazy=True, cascade="delete"))




