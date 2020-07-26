import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *

engine = create_engine(
    "postgres://tlwyypeknccxmj:56575f0a7f2c48fd46b9d4820e449677476a301411fe31e5c3840a7dfb3f072d@ec2-52-87-135-240.compute-1.amazonaws.com:5432/daglbknsce9fgh")
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
