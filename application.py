from flask import Flask, session, render_template, request, redirect, url_for, g, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_bcrypt import Bcrypt
import datetime
import requests

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = 'fuckallinthepussy'
bcrypt = Bcrypt(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(
    "postgres://nnktecvpjegvim:2f055e202a55d4207b0d9d694a3d98651aa9a96227a2692d0a4b9ff2680bf3e8@ec2-34-233-226-84"
    ".compute-1.amazonaws.com:5432/db5ar3itlbrsdh")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project 1: TODO"


@app.route("/login")
def login():
    return render_template("login.html", message="")


@app.route("/signup")
def signup():
    return render_template("signup.html", message="")


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = db.execute(f"SELECT * FROM users WHERE id={session['user_id']}").fetchone()
        g.user = user


@app.route("/inside", methods=["POST", "GET"])
def userpage():
    if request.method == "POST":
        session.pop('g.user.id', None)
        username = str(request.form.get("username"))
        password = str(request.form.get("password"))

        user = db.execute(f"SELECT * FROM users WHERE username='{username}'").fetchone()

        if user is None:
            return render_template("login.html", message="No user with that username found!")

        elif bcrypt.check_password_hash(user.passwordhash, password) is False:
            return render_template("login.html", message="Password entered is incorrect")

        else:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

    else:
        return redirect(url_for('login'))


@app.route("/signup/tologinredirect", methods=["POST"])
def loginredirect():
    username = str(request.form.get("username"))
    password = str(request.form.get("password"))
    copassword = str(request.form.get("confirmpassword"))
    mail = str(request.form.get("email"))
    '''I need to add a feature if mailid already exists then use a different mailid'''
    if username == "" or password == "" or copassword == "" or mail == "":
        return render_template("signup.html", message="Input cannot be empty")
    else:
        if db.execute(f"SELECT * FROM users WHERE username='{username}'").rowcount != 0:
            return render_template("signup.html", message=f"{username} already exists,Choose different username.")
        elif password != copassword:
            return render_template("signup.html", message="Password and confirm password not matched")
        else:
            passwordstored = bcrypt.generate_password_hash(password).decode('utf-8')
            db.execute(
                f"INSERT INTO users (username,passwordhash,email) VALUES ('{username}','{passwordstored}','{mail}')")
            db.commit()
            return render_template("login.html", message="Signup successful,You can login now!!! ")


@app.route("/logout", methods=["GET"])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route("/profile")
def profile():
    x = datetime.datetime.now()
    date = x.date()
    time = x.time()
    if not g.user:
        return redirect(url_for('login'))
    else:
        return render_template("profile.html", username=g.user.username, user_id=g.user.id, user_mail=g.user.email,
                               date=date, time=time, message="Your search results will be shown here!!")


@app.route("/booksearch", methods=["POST", "GET"])
def booksearch():
    x = datetime.datetime.now()
    date = x.date()
    time = x.time()
    title = request.form.get("title")
    author = request.form.get("author")
    year = request.form.get("year")
    isbn = request.form.get("isbn")
    books = db.execute(f"SELECT * FROM books WHERE year LIKE '%{year}%' AND isbn LIKE '%{isbn}%'")
    if books.fetchone() is None:
        return render_template("profile.html", username=g.user.username, user_id=g.user.id, user_mail=g.user.email,
                               date=date, time=time, message="Nothing found with given context")
    else:
        book1 = list(books.fetchall())
        if len(title) == 0 and len(author) == 0:

            return render_template("profile1.html", username=g.user.username, user_id=g.user.id, user_mail=g.user.email,
                                   date=date, time=time, message=book1)
        elif len(title) != 0 and len(author) != 0:
            message = []
            for book in book1:
                if title.lower() in book.title and author.lower() in book.author:
                    message.append(book)
            print(message)
            return render_template("profile1.html", username=g.user.username, user_id=g.user.id, user_mail=g.user.email,
                                   date=date, time=time, message=message)
        else:
            if len(title) == 0:
                message = []
                for book in book1:
                    if author.lower() in book.author.lower():
                        message.append(book)
                print(message)
                return render_template("profile1.html", username=g.user.username, user_id=g.user.id,
                                       user_mail=g.user.email,
                                       date=date, time=time, message=message)

            else:
                message = []
                for book in book1:
                    if title.lower() in book.title.lower():
                        message.append(book)
                print(message)
                return render_template("profile1.html", username=g.user.username, user_id=g.user.id,
                                       user_mail=g.user.email,
                                       date=date, time=time, message=message)


@app.route("/books/<int:bid>")
def details(bid):
    book = db.execute(f"SELECT * FROM books WHERE id = {bid}").fetchone()
    print(book)
    if book is None:
        return "No such book in database"
    print(type(bid))
    isbn = book.isbn
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "Pn7DlC42USFpGBgmC3sg", "isbns": isbn})
    if res.status_code == 200:
        average_rating = ((((res.json())["books"])[0])['average_rating'])
        ratings_count = ((((res.json())["books"])[0])['work_ratings_count'])
        reviews = db.execute(f"SELECT * FROM reviews WHERE book_id={bid} ORDER BY id DESC").fetchall()
        return render_template("details.html", book=book, average=average_rating, message="", reviews=reviews,
                               number=ratings_count)
    else:
        return render_template("error.html", message="Some error caught in JSON parser.")


@app.route("/reviews/<int:bid>", methods=["POST", "GET"])
def submission(bid):
    comment = request.form.get('comment')
    user_id = g.user.id
    book_id = bid
    username = g.user.username
    rating = request.form.get('checkbox')
    book = db.execute(f"SELECT * FROM books WHERE id = {bid}").fetchone()
    isbn = book.isbn
    if comment == "":
        return redirect(url_for('details', bid=book_id))
    else:
        if db.execute(f"SELECT * FROM reviews WHERE book_id={book_id} AND user_id={user_id}").fetchone() is None:
            db.execute(
                f"INSERT INTO reviews (review,rating,user_id,book_id,username) VALUES ('{comment}',{rating},{user_id},{book_id},'{username}')")
            db.commit()
            return redirect(url_for('details', bid=book_id))
        else:
            res = requests.get("https://www.goodreads.com/book/review_counts.json",
                               params={"key": "Pn7DlC42USFpGBgmC3sg", "isbns": isbn})
            if res.status_code == 200:
                average_rating = ((((res.json())["books"])[0])['average_rating'])
                ratings_count = ((((res.json())["books"])[0])['work_ratings_count'])
                reviews = db.execute(f"SELECT * FROM reviews WHERE book_id={book_id} ORDER BY id DESC").fetchall()
                return render_template("details.html", book=book, average=average_rating, message="Looks like you have "
                                                                                                  "already submitted "
                                                                                                  "review "
                                                                                                  "for this book",
                                       reviews=reviews,
                                       number=ratings_count)
            else:
                return render_template("error.html", message="Some error caught in JSON parser.")


@app.route("/api/<isbn>")
def api(isbn):
    books = db.execute(f"SELECT * FROM books WHERE isbn = '{isbn}'").fetchone()
    print(books)
    if books is None:
        return "Invalid isbn"
    title = books.title
    author = books.author
    year = books.year
    review_count = db.execute(f"SELECT COUNT(*) FROM reviews WHERE book_id = {books.id}").fetchone()
    print(review_count[0])
    average_score = db.execute(f"SELECT AVG(rating) FROM reviews WHERE book_id = {books.id}").fetchone()
    if average_score[0] is None:
        print(average_score[0])
        return jsonify({"title": title, "author": author, "year": year, "isbn": isbn, "review_count": review_count[0],
                        "average_score": 0})

    print(average_score[0])
    return jsonify({"title": title, "author": author, "year": year, "isbn": isbn, "review_count": review_count[0],
                    "average_score": float(average_score[0])})


@app.errorhandler(404)
def error(e):
    return render_template("error.html", message="Looks like you have requested something wrong!!")
@app.errorhandler
def error1(e):
    return "invalid isbn "

if __name__ == "__main__":
    app.run(debug=True, port=5432)
