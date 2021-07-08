from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

dummy = Flask(__name__)
dummy.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://xjlxshxuakpech' \
                                 ':ddf775f0c9915886bff67a43ecba785c78dc9f46e6ddb3645474d7759de9f62e@ec2-3-214-136-47' \
                                 '.compute-1.amazonaws.com:5432/d9nr10ubldfvmp'

dummy.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(dummy)


class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column('isbn', db.String, nullable=False)
    title = db.Column('title', db.String, nullable=False)
    author = db.Column('author', db.String, nullable=False)
    year = db.Column('year', db.String, nullable=False)


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username', db.String, nullable=False, unique=True)
    password = db.Column('password', db.String, nullable=False)
    email = db.Column('email', db.String, nullable=False, unique=True)


class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column('review', db.String, nullable=False)
    rating = db.Column('rating', db.Integer, nullable=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column('book_id', db.Integer, db.ForeignKey("books.id"), nullable=False)
    username = db.Column('username', db.String, nullable=False)


def main():
    db.create_all()


with dummy.app_context():
    main()
