from utils.json_interpreter import *
from Abbyy_Translator.Translator import *


class TranslationInserter:

    def __init__(self, word_freq_list_filepath=None):
        if word_freq_list_filepath is None:
            word_freq_list_filepath = 'word_lists/masterrussian_1000_words_cleaned.csv'
        self.Translator = Translator('Njc4ZmFjZDYtN2VhZC00OTk4LWE3NjItMzhjOGY3MmRhYjNhOmVjNjk3YTMwMjM5NDQ2MjdiM2JmYzU2N2VhNDlhZjBm')
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
        book = json_to_book(raw_text)

        # Add in frequencies and translation if high enough

        for ch_num, chapter in enumerate(book.chapters):
            for p_num, paragraph in enumerate(chapter.paragraphs):
                for word in paragraph.words:
                    print(f'processing {word.lemma}\n'
                          f'ch: {ch_num}; p: {p_num}')
                    translation, abbyy_type = self.Translator.get_translation(word.lemma)
                    word.translation = translation
                    word.frequency = self.get_word_frequency(word.lemma)

        new_book_json = book_to_json(book)
        print('writing new book with translations to file')
        with open('cleaned_pickles/ivan_ilyich_book_with_translations.json', 'wb') as f:
            f.write(new_book_json)


    def get_word_frequency(self, word):
        try:
            return self.word_freq_list[word]['ipm']
        except KeyError:
            return float('inf')

ti = TranslationInserter()
ti.insert_translations("cleaned_pickles/ivan_ilyich_book.json")