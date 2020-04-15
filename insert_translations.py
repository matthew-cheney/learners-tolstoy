from utils.json_interpreter import *
from Abbyy_Translator.Translator import *
import re


class TranslationInserter:

    def __init__(self, word_freq_list_filepath=None):
        if word_freq_list_filepath is None:
            word_freq_list_filepath = 'word_lists/masterrussian_32000_words_cleaned.csv'
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

    def insert_translations(self, json_filename, BOOK_FILENAME):
        with open(json_filename, 'r') as f:
            raw_text = f.read()
        book = json_to_book_footnotes_separate(raw_text)

        # Add in frequencies and translation
        num_chapters = len(book.chapters)
        for ch_num, chapter in enumerate(book.chapters):
            # if ch_num == 1:
            #     break
            # if ch_num < 6:
            #     continue
            print(f'processing {ch_num} / {num_chapters}')
            for p_num, paragraph in enumerate(chapter.paragraphs):
                for word in paragraph.words:
                    print(f'processing {word.lemma}\n'
                          f'ch: {ch_num}; p: {p_num}')
                    if len(re.findall(r'[а-яА-Я]', word.lemma)) == 0:
                        translation, abbyy_type = "not Russian", "foreign"
                        # print(f'skipping {word.lemma} - not Russian')
                    else:
                        translation, abbyy_type = self.Translator.get_translation(word.lemma)
                    word.translation = translation
                    word.frequency = self.get_word_frequency(word.lemma)
                    if word.footnote != None:
                        for ft_word in word.footnote:
                            translation, abbyy_type = self.Translator.get_translation(ft_word.lemma)
                            ft_word.translation = translation
                            ft_word.frequency = self.get_word_frequency(ft_word.lemma)

        new_book_json = book_to_json(book)
        print('writing new book with translations to file')
        with open(f'cleaned_pickles/{BOOK_FILENAME}_book_with_translations.json', 'wb') as f:
            f.write(new_book_json)

    def get_word_frequency(self, word):
        try:
            return self.word_freq_list[word]['ipm']
        except KeyError:
            return float('inf')


def insert_translations_outer(BOOK_FILENAME):
    ti = TranslationInserter()
    ti.insert_translations(f"cleaned_pickles/{BOOK_FILENAME}_book.json", BOOK_FILENAME)


if __name__ == '__main__':

    BOOK_FILENAMES = [
        'ivan_ilyich',
        'cossacks',
        'resurrection_p1',
        'resurrection_p2',
        'resurrection_p3',
        # 'anna_karenina_p1'
    ]

    for BOOK_FILENAME in BOOK_FILENAMES:
        insert_translations_outer(BOOK_FILENAME)

    # from sys import argv
    # if len(argv) < 2:
    #     print(f'USAGE: {argv[0]} <filename (not path)>')
    #     exit(1)
    # insert_translations_outer(argv[1])
