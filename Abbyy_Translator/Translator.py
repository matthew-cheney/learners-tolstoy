import json
import sys
import os
import time

import requests
import sqlite3
import datetime

from Abbyy_Translator.Exceptions import *


ABBYY_CHAR_LIMIT = 50000

class Translator:
    def __init__(self, api_key):
        self.limit_reached = False
        # Set up the api key
        self.api_key = api_key
        self.srcD = 1049  # Russian
        self.dstD = 1033  # English

        # Set up character tracker

        self._read_char_tracker()

        self._429s = [0]

        # Set up the volatile key
        self.volatile_filename = 'Abbyy_Translator/volatile_key.txt'
        try:
            self.volatile_key = self._load_volatile_key()
        except FileNotFoundError:
            self.volatile_key = self._get_new_volatile_key()

        # Set up the database
        self.db_filename = 'Abbyy_Translator/saved_translations_mini.db'
        if not os.path.exists(self.db_filename):
            raise DBNotFoundException(f'saved_translations db not found. Create db at {self.db_filename}')
        self.conn = sqlite3.connect(self.db_filename)
        self.c = self.conn.cursor()

    def _read_char_tracker(self):
        with open('Abbyy_Translator/character_tracker.txt', 'r') as f:
            raw_text = f.read()
        date, count, *args = raw_text.split('\n')
        if date == datetime.datetime.now().date().__str__():
            # Same date as today, load counter
            self.char_counter = int(count)
        else:
            # Different date - reset counter
            self.char_counter = 0
            self._write_char_tracker()

    def _write_char_tracker(self):
        with open('character_tracker.txt', 'w') as f:
            with open('character_tracker.txt', 'w') as f:
                print(datetime.datetime.now().date().__str__(), self.char_counter, sep='\n', file=f)

    def _load_volatile_key(self):
        if not os.path.exists(self.volatile_filename):
            raise FileNotFoundError(self.volatile_filename)
        with open(self.volatile_filename, 'r') as f:
            volatile_key = f.read()
        return volatile_key

    def _get_new_volatile_key(self):
        data = {'Authorization': f'Basic {self.api_key}'}
        r = requests.post(
            url='https://developers.lingvolive.com/api/v1.1/authenticate',
            headers=data)
        with open(self.volatile_filename, 'w') as f:
            print(r.text, file=f, end='')
        return self._load_volatile_key()

    def get_translation(self, word):
        res = self._retrieve_translation(word)
        translation, type = self.parse_result_mini(res, word)
        return translation, type

    def _retrieve_translation(self, word):
        if word is None:
            return dict()
        result = self._get_word_from_database(word)
        if result is None:
            # Not in db yet, query Abbyy api
            if self.char_counter + len(word) >= ABBYY_CHAR_LIMIT:
                raise(AbbyyCharLimitReachedException())
            print("querying Abbyy api")
            self._query_abbyy(word)
            return self.get_translation(word)
        else:
            # word already in db
            try:
                return json.loads(result[0].decode("utf-8"))
            except AttributeError:
                return json.loads(result[0])

    def _write_translation_to_db(self, word: str, abbyy_result: str):
        # Check if word already in db
        self.c.execute("SELECT * FROM translations WHERE word=?", (word,))
        if (self.c.fetchone() is not None):
            raise WordAlreadyInDatabaseException(f'\'{word}\' already in {self.db_filename}')

        params = (datetime.datetime.now(), word, abbyy_result,)
        self.c.execute("INSERT INTO translations VALUES (?,?,?)", params)
        self.conn.commit()

    def _get_word_from_database(self, word):
        try:
            self.c.execute("SELECT abbyy_result FROM translations WHERE word=?", (word,))
            db_result = self.c.fetchone()
            if db_result is None:
                raise WordNotFoundInDatabaseException(f'\'{word}\' not found in {self.db_filename}')
            return db_result
        except WordNotFoundInDatabaseException:
            return None

    def _query_abbyy(self, word):
        # Query abbyy
        headers = {'Authorization': f'Bearer {self.volatile_key}'}
        url = f'https://developers.lingvolive.com/api/v1/Minicard?text={word}&srcLang={self.srcD}&dstLang={self.dstD}'
        self.char_counter += len(word)
        self._write_char_tracker()
        # time.sleep(2)
        print('sending request')
        r = requests.get(url=url, headers=headers)
        print(f'result received - {r.status_code}')

        # Check if volatile key was good
        if r.status_code == 200:
            self._429s[-1] += 1
            self.limit_reached = False
            # Volatile key good - write to db and return
            self._write_translation_to_db(word, r.content)
            return r.content
        elif r.status_code == 404:
            self._429s[-1] += 1
            self.limit_reached = False
            mock_content = f'{{"SourceLanguage":1049,"TargetLanguage":1033,"Heading":"{word}","Translation":{{"Heading":"{word}","Translation":"NO TRANSLATION FOUND","DictionaryName":"LingvoUniversal (Ru-En)","SoundName":"None","Type":0,"OriginalWord":""}},"SeeAlso":[]}}'
            self._write_translation_to_db(word, mock_content)
            return mock_content
        elif r.status_code == 401:
            # Volatile key was bad
            # Get new volatile key
            self.volatile_key = self._get_new_volatile_key()
            # Query again
            return self._query_abbyy(word)
        else:
            print(self._429s)
            self._429s.append(0)
            if self.limit_reached:
                print('429 hit twice - - - - - - - - - - - - - - - - -')
                for remaining in range(300, 0, -1):
                    sys.stdout.write("\r")
                    sys.stdout.write(
                        "{:2d} seconds remaining.".format(remaining))
                    sys.stdout.flush()
                    time.sleep(1)
                return self._query_abbyy(word)
            else:
                print('429 hit once - - - - - - - - - - - - - - - -')
                for remaining in range(300, 0, -1):
                    sys.stdout.write("\r")
                    sys.stdout.write(
                        "{:2d} seconds remaining.".format(remaining))
                    sys.stdout.flush()
                    time.sleep(1)
                self.limit_reached = True
                return self._query_abbyy(word)


    def parse_result_mini(self, res, word):
        words = ''
        if isinstance(res, tuple):
            return res[0],res[1]
        try:
            words = res['Translation']['Translation']
            type = res['Translation']['Type']
        except KeyError:
            return 'error in parsing'
        return words, type

def parse_result(res, word):
    words = []
    comments = []
    for each_res in res:
        if each_res['Dictionary'] != 'LingvoUniversal (Ru-En)':
            continue
        if each_res['Title'] != word:
            continue
        Body = each_res['Body']
        typed = False
        for each_body in Body:
            if 'Type' in each_body:
                typed = True
        for each_body in Body:
            if typed == True and 'Type' in each_body:
                if each_body['Type'] == 3 or each_body['Type'] == 1 or \
                    each_body['Type'] == None:
                    Items = each_body['Items']
                    for each_item in Items:
                        for each_markup in each_item['Markup']:
                            if each_markup['Node'] == 'Paragraph':
                                for each_each in each_markup['Markup']:
                                    if each_each['Node'] != 'Text':
                                        continue
                                    words.append(each_each['Text'])
                            if each_markup['Node'] == 'Comment':
                                for each_each in each_markup['Markup']:
                                    if each_each['Node'] != 'Text':
                                        continue
                                    comments.append(each_each['Text'])

            elif typed == False:
                if each_body['Node'] != 'Paragraph':
                    continue
                for each_markup in each_body['Markup']:
                    if each_markup['Node'] == 'Text':
                        words.append(each_markup['Text'])

    return words, comments


# t = Translator('')
"""russ_words = ['поход',
              'лук',
              'говорить',
              'видеоигра',
              'потом',
              'свидетельствовать',
              'дескать',
              'часы',
              'коммунизм',
              'обворовывать',
              'селить',
              'призываться'
              ]
for russ_word in russ_words:
    res = t.get_translation(russ_word)
    words, type = t.parse_result_mini(res, russ_word)
    # words, comments = parse_result(res, russ_word)
    print(f'word: {russ_word}\n'
          f'words: {words}\n'
          f'type: {type}\n'
          # f'comments: {comments}'
          )"""