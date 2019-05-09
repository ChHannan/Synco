from time import time
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """User database model
    Stores all the users information."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    confirmed_on = db.Column(db.Integer)
    files = db.relationship('File', backref='uploader', lazy='dynamic')
    token = db.relationship('Token', backref='auth', lazy='dynamic')
    avatar = db.relationship('Avatar', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Avatar(db.Model):
    """Avatar database model
    Stores users' avatars information."""
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String, default='/static/avatars/0.png')
    counter = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Filename {}>'.format(self.avatar)


class File(db.Model):
    """File database model
    Stores all the uploaded files information."""
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(128), index=True)
    repo = db.Column(db.String(7), default='public')
    type = db.Column(db.String(64), default='misc')
    path = db.Column(db.String(255))
    timestamp = db.Column(db.Integer, default=int(time()))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    open_file = db.relationship('Token', backref='file', lazy='dynamic')

    def __repr__(self):
        return '<Filename {}>'.format(self.filename)


class Token(db.Model):
    """Token database model
    Stores information about every token generated.
    From pagination to confirmation and resetting passwords, this database is used in everything."""
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(128), index=True)
    type = db.Column(db.String(10))
    timestamp = db.Column(db.Integer, default=int(time()))
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Token {}>'.format(self.token)


@login.user_loader
def load_user(id):
    """
    Logins user
    :param id: User id as defined in database model.
    :return: returns the user database.
    """
    return User.query.get(int(id))
