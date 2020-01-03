from app_api import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    permission = db.Column(db.String(100), default='User')
    addresses = db.relationship('Posts', backref='users', lazy=True)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    post_body = db.Column(db.Text(), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)