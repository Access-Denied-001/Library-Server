from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

dummy = Flask(__name__)
dummy.config[
    'SQLALCHEMY_DATABASE_URI'] = 'postgres://tlwyypeknccxmj:56575f0a7f2c48fd46b9d4820e449677476a301411fe31e5c3840a7dfb3f072d@ec2-52-87-135-240.compute-1.amazonaws.com:5432/daglbknsce9fgh'
dummy.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(dummy)


class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column('isbn', db.String, nullable=False)
    title = db.Column('title', db.String, nullable=False)
    author = db.Column('author', db.String, nullable=False)
    year = db.Column('year', db.String, nullable=False)


class Credential(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)


class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    review = db.Column('review', db.String, nullable=False)
    rating = db.Column('rating',db.Integer,nullable=False)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column('book_id', db.Integer, db.ForeignKey("books.id"), nullable=False)
    username = db.Column('username', db.String, nullable=False)



def main():
    db.create_all()


with dummy.app_context():
    main()
