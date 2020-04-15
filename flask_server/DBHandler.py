import sqlite3
import datetime
import uuid

def write_book_to_db(db_filename, title, author, book_json):
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()
    book_id = uuid.uuid4().hex
    params = (datetime.datetime.now(), book_id, title, author, book_json)
    c.execute("INSERT INTO books VALUES (?,?,?,?)", params)
    conn.commit()
    conn.close()
    return book_id

def get_book_json(db_filename, book_id):
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()
    c.execute("SELECT json FROM books WHERE id=?", (book_id,))
    db_result = c.fetchone()
    conn.close()
    if db_result is None:
        return 0
    else:
        return db_result[0]

def get_all_books(db_filename):
    conn = sqlite3.connect(db_filename)
    c = conn.cursor()
    c.execute("SELECT title, author, id, difficulty FROM books")
    db_result = c.fetchall()
    conn.close()
    if db_result is None:
        return []
    else:
        return db_result
