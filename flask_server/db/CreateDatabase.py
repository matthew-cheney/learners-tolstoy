import sqlite3
import sys
import os

if len(sys.argv) > 1:
    print(f'loading db_filename: {sys.argv[1]}')
    db_filename = sys.argv[1]
else:
    print('using default db_filename: bookshelf.db')
    db_filename = 'bookshelf.db'

if os.path.exists(db_filename):
    print(f'{db_filename} already exists')
    exit(1)

print(f'establishing connections to {db_filename}')
conn = sqlite3.connect(db_filename)
c = conn.cursor()

create_tables_string = """
CREATE TABLE books (date text, id text, title text, author text, json text)
"""

print('creating table(s)')
c.execute(create_tables_string)
conn.commit()

print('done')