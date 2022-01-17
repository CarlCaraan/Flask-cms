from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    password = db.Column(db.String(150))
    usertype = db.Column(db.String(10))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    posts = db.relationship('Post', backref='user', passive_deletes="True") # relationship of user and posts
    comments = db.relationship('Comment', backref='user', passive_deletes="True") # relationship of user and comments
    likes = db.relationship('Like', backref='user', passive_deletes="True") # relationship of user and comments

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable="False")
    comments = db.relationship('Comment', backref='post', passive_deletes=True) # relationship of post and comments
    likes = db.relationship('Like', backref='post', passive_deletes="True") # relationship of user and comments

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable="False")
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable="False")

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable="False")
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable="False")