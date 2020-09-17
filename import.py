import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

engine = create_engine(
    "postgres://jboqoljyxnfxyr:12f51c7443e256dc9df95404a8ceac0b56aa156c9455a599e1273f152ff31b47@ec2-52-0-155-79.compute-1.amazonaws.com:5432/diehcu9kc9u7vh")
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
