import sys
import os
import requests
import sqlite3
import datetime

from Abbyy_Translator.Exceptions import *


class Translator:
    def __init__(self, api_key):
        # Set up the api key
        self.api_key = api_key
        self.srcD = 1049  # Russian
        self.dstD = 1033  # English

        # Set up the volatile key
        self.volatile_filename = 'volatile_key.txt'
        try:
            self.volatile_key = self._load_volatile_key()
        except FileNotFoundError:
            self.volatile_key = self._get_new_volatile_key()

        # Set up the database
        self.db_filename = 'saved_translations.db'
        if not os.path.exists(self.db_filename):
            raise DBNotFoundException('saved_translations db not found. Create db at saved_translations.db')
        self.conn = sqlite3.connect('saved_translations.db')
        self.c = self.conn.cursor()

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
        result = self._get_word_from_database(word)
        if result is None:
            # Not in db yet, query Abbyy api
            print("querying Abbyy api")
            result = self._query_abbyy(word)
        else:
            # word already in db
            return result[0]

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
        url = f'https://developers.lingvolive.com/api/v1/Translation?text={word}&srcLang={self.srcD}&dstLang={self.dstD}'
        r = requests.get(url=url, headers=headers)

        # Check if volatile key was good
        if r.status_code == 200:
            # Volatile key good - write to db and return
            self._write_translation_to_db(word, r.content)
            return r.content
        else:
            # Volatile key was bad
            # Get new volatile key
            self._get_new_volatile_key()
            # Query again
            return self._query_abbyy(word)
