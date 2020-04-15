import re
import sqlite3

DB_FILENAME = 'Abbyy_Translator/saved_translations_mini.db'

conn = sqlite3.connect(DB_FILENAME)
try:
    c = conn.cursor()
    c.execute("""
    SELECT * FROM translations
    """)
    db_words = c.fetchall()
finally:
    conn.close()

translation_found = 0
no_translation_found = 0
nt = list()

import json

for word in db_words:
    abbyy_result = json.loads(word[2])
    if len(re.findall(r'[а-яА-Я]', word[1])) == 0:
        continue
    if abbyy_result['Translation']['Translation'] == 'NO TRANSLATION FOUND':
        no_translation_found += 1
        nt.append(word[1])
    else:
        translation_found += 1

print(f'translation_found: {translation_found}\n'
      f'no_translation_found: {no_translation_found}')
print(nt)