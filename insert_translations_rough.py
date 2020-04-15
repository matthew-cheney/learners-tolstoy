import stanfordnlp
import re

from utils.json_interpreter import *
from Abbyy_Translator.Translator import *


class TranslationInserter:

    def __init__(self, word_freq_list_filepath=None):
        if word_freq_list_filepath is None:
            word_freq_list_filepath = 'word_lists/masterrussian_1000_words_cleaned.csv'
        with open('Abbyy_Translator/api_key.txt', 'r') as f:
            api_key = f.read()
            api_key.replace('\n','')
        self.Translator = Translator(api_key)
        with open(word_freq_list_filepath, 'r') as f:
            raw_text = f.read()
        self.word_freq_list = dict()
        for line in raw_text.split('\n'):
            if line == '':
                continue
            rank, ipm, lemma, pos = line.split(',')
            self.word_freq_list[lemma] = {'rank': int(rank),
                                     'ipm': float(ipm),
                                     'lemma': lemma,
                                     'pos': pos}

    def insert_translations(self, json_filename):
        with open(json_filename, 'r') as f:
            raw_text = f.read()

        nlp = stanfordnlp.Pipeline(lang='ru')


        total_p = len(raw_text.split('\n'))

        for p_num, paragraph in enumerate(raw_text.split('\n')):
            if p_num < 6130:
                continue
            if len(paragraph) == 0 or paragraph is None or paragraph == ' ' or paragraph == '  ':
                continue
            doc = nlp(paragraph)
            word_count = 0
            for sentence in doc.sentences:
                for word in sentence.words:
                    print(f'processing {word.lemma}\n'
                          f'p: {p_num} / {total_p}; word: {word_count}')
                    word_count += 1
                    if len(re.findall(r'[а-яА-Я]', word.lemma)) == 0:
                        translation, abbyy_type = "not Russian", "foreign"
                        print(f'skipping {word.lemma} - not Russian')
                    else:
                        self.Translator.get_translation(word.lemma)

    def get_word_frequency(self, word):
        try:
            return self.word_freq_list[word]['ipm']
        except KeyError:
            return float('inf')

import warnings

warnings.filterwarnings("ignore")

BOOK_FILENAME = 'war_and_peace_rough.txt'
ti = TranslationInserter()
ti.insert_translations(f"cleaned_json/{BOOK_FILENAME}")
