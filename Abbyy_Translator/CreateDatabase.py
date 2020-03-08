import sqlite3
import sys

if len(sys.argv) > 1:
    print(f'loading db_filename: {sys.argv[1]}')
    db_filename = sys.argv[1]
else:
    print('using default db_filename: saved_translations.db')
    db_filename = 'saved_translations.db'

print(f'establishing connections to {db_filename}')
conn = sqlite3.connect(db_filename)
c = conn.cursor()

create_tables_string = """
CREATE TABLE translations (date text, word text, abbyy_result text)
"""

print('creating table(s)')
c.execute(create_tables_string)
conn.commit()

print('done')