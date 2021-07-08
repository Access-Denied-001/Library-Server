import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

engine = create_engine("postgres://xjlxshxuakpech:ddf775f0c9915886bff67a43ecba785c78dc9f46e6ddb3645474d7759de9f62e"
                       "@ec2-3-214-136-47.compute-1.amazonaws.com:5432/d9nr10ubldfvmp")
db = scoped_session(sessionmaker(bind=engine))


def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for small in list(reader):
        isbn = small[0]
        title = small[1]
        author = small[2]
        year = small[3]
        if isbn == "isbn":
            print('cannot add this')
        else:
            db.execute("INSERT INTO books ( isbn, title, author,year) VALUES (:isbn,:title,:author,:year);",{'isbn':isbn,'title':title,'author':author,'year':year})
            print(f"{isbn},{title},{author},{year}")
    db.commit()


if __name__ == "__main__":
    main()
