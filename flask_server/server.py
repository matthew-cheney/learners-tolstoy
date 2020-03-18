import sqlite3

from flask import Flask, render_template
from flask_server import DBHandler
from utils.json_interpreter import json_to_book
from json.decoder import JSONDecodeError

app = Flask(__name__)

db_filename = 'db/bookshelf.db'

@app.route('/')
def hello_world():
    all_books = DBHandler.get_all_books(db_filename)
    return render_template('bookshelf.html', all_books=all_books)

@app.route('/book/<book_id>/<chapter_number>')
def get_chapter(book_id, chapter_number):
    try:
        chapter_number = int(chapter_number)
    except ValueError:
        return 'invalid chapter number'
    book = _get_book_from_db(book_id)
    try:
        chapter = book.chapters[chapter_number]
    except IndexError:
        return 'invalid chapter number'
    return render_template('chapter.html', title=book.title, book=book, chapter=chapter)

@app.route('/book/<book_id>')
def get_book(book_id):
    book = _get_book_from_db(book_id)
    return render_template('book.html', book=book)

def _get_book_from_db(book_id):
    book_json = DBHandler.get_book_json(db_filename, book_id)
    if isinstance(book_json, int):
        return f'no book found with id {book_id}'
    try:
        book = json_to_book(book_json)
        return book
    except (TypeError, JSONDecodeError):
        return 'something went wrong'