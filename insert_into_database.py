import sqlite3

from get_book_difficulty import get_book_frequency
from utils.json_interpreter import *
import datetime
import uuid

DB_FILENAME = 'flask_server/db/bookshelf.db'

def insert_book_into_db(BOOK_FILENAME):

    with open(f'cleaned_json/{BOOK_FILENAME}_book_with_translations.json', 'r') as f:
        raw_text = f.read()

    book = json_to_book(raw_text)

    conn = sqlite3.connect(DB_FILENAME)
    try:
        c = conn.cursor()

        # Check if title/author combo already in database
        c.execute("""
        SELECT * FROM books WHERE title=? AND author=?;
        """, (
            book.title,
            book.author
        ))
        if len(c.fetchall()) > 0:
            return False

        # (date text, id text, title text, author text, json text, difficulty int)
        c.execute("""
        INSERT INTO books VALUES (?,?,?,?,?,?);
        """, (
            datetime.datetime.now(),
            uuid.uuid4().hex,
            book.title,
            book.author,
            raw_text,
            get_book_frequency(BOOK_FILENAME)
        ))
        conn.commit()
        return True
    finally:
        conn.close()






if __name__ == '__main__':

    BOOK_FILENAMES = [
        'ivan_ilyich',
        'cossacks',
        'resurrection_p1',
        'resurrection_p2',
        'resurrection_p3',
        # 'anna_karenina_p1'
    ]

    for BOOK_FILENAME in BOOK_FILENAMES:
        print(f'processing {BOOK_FILENAME}')
        insert_book_into_db(BOOK_FILENAME)

    # from sys import argv
    # if len(argv) < 2:
    #     print(f'USAGE: {argv[0]} <filename (not path)>')
    #     exit(1)
    # insert_book_into_db(argv[1])
