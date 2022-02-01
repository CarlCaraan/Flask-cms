from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    company = db.Column(db.String(150))
    password = db.Column(db.String(150))
    usertype = db.Column(db.String(10))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    # relationship of user and posts
    posts = db.relationship('Post', backref='user', passive_deletes="True")
    # comments = db.relationship('Comment', backref='user', passive_deletes="True") # relationship of user and comments
    # relationship of user and comments
    likes = db.relationship('Like', backref='user', passive_deletes="True")


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    # date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    date_created = db.Column(db.DateTime, default=datetime.now())
    date_updated = db.Column(db.DateTime(
        timezone=True), onupdate=datetime.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable="False")
    # comments = db.relationship('Comment', backref='post', passive_deletes=True) # relationship of post and comments
    # relationship of user and comments
    likes = db.relationship('Like', backref='post', passive_deletes="True")
    location = db.Column(db.Text, nullable=False)
    location1 = db.Column(db.Text, nullable=False)
    salary = db.Column(db.Text, nullable=True)
    salary1 = db.Column(db.Text, nullable=True)
    level = db.Column(db.Text, nullable=False)
    experience = db.Column(db.Text, nullable=False)
    specialization = db.Column(db.Text, nullable=False)
    qualification = db.Column(db.Text, nullable=True)
    qualification1 = db.Column(db.Text, nullable=True)
    qualification2 = db.Column(db.Text, nullable=True)
    qualification3 = db.Column(db.Text, nullable=True)
    qualification4 = db.Column(db.Text, nullable=True)
    jobtype = db.Column(db.Text, nullable=False)

# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(200), nullable=False)
#     date_created = db.Column(db.DateTime(timezone=True), default=func.now())
#     author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable="False")
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable="False")


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable="False")
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable="False")
