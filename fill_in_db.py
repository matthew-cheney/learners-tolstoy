import re
import sqlite3
from google.cloud import translate_v2 as translate
import datetime

DB_FILENAME = 'Abbyy_Translator/saved_translations_mini.db'

language_code = 'en'

api_dictionary = translate.Client()


x = 0
conn = sqlite3.connect(DB_FILENAME)
try:
    c = conn.cursor()
    c.execute("""
    SELECT * FROM translations
    """)
    db_words = c.fetchall()


    translation_found = 0
    no_translation_found = 0
    nt = list()

    char_counter = 0

    import json
    numWords = len(db_words)
    for word_i, word in enumerate(db_words):
        abbyy_result = json.loads(word[2])
        if len(re.findall(r'[а-яА-Я]', word[1])) == 0:
            continue
        if abbyy_result['Translation']['Translation'] == 'NO TRANSLATION FOUND':
            # no translation found
            print(f'translating {word[1]}: {word_i} / {numWords}')
            google_res = api_dictionary.translate(
                    word[1], target_language=language_code)
            char_counter += len(word[1])
            abbyy_result['Translation']['Translation'] = google_res['translatedText']
            abbyy_result['Translation']['DictionaryName'] = 'GoogleTranslate (v2)'
            c.execute("""
            UPDATE translations
            SET date=?,
                abbyy_result=?
            WHERE word=?
            """, (datetime.datetime.now(), json.dumps(abbyy_result, ensure_ascii=False), word[1]))
            conn.commit()
finally:
    conn.close()
    print('chars translated:', char_counter)
print(f'translation_found: {translation_found}\n'
      f'no_translation_found: {no_translation_found}')
print(nt)