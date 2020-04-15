import re

from utils.json_interpreter import *

FREQ_CUTOFF = 200

def get_book_frequency(BOOK_FILENAME):
    # Get all text from file
    with open(f'cleaned_pickles/{BOOK_FILENAME}_book_with_translations.json', 'r') as f:
        raw_text = f.read()

    book = json_to_book(raw_text)

    # Count up all word frequencies, track infinities separate (if not punct or foreign)
    # Only count each word once (i.e. no duplicates)
    freq_sum = 0
    freq_words = set()
    inf_russ_words = set()
    for chapter in book.chapters:
        for paragraph in chapter.paragraphs:
            for word in paragraph.words:
                if word.lemma not in freq_words and word.frequency != float('inf') and word.frequency < FREQ_CUTOFF:
                    freq_sum += word.frequency
                    freq_words.add(word.lemma)
                elif word.frequency == float('inf') and word.lemma not in inf_russ_words:
                    if contains_cyrillic(word.lemma):
                        inf_russ_words.add(word.lemma)
    # print(f'Book: {BOOK_FILENAME}\n'
    #       f'Freq sum: {freq_sum}\n'
    #       f'Num words: {len(freq_words)}\n'
    #       f'Normalized: {freq_sum / len(freq_words)}\n'
    #       f'Inf Russ words: {len(inf_russ_words)}\n')

    return freq_sum / len(freq_words)



def contains_cyrillic(text):
    return len(re.findall(r'[а-яА-Я]', text)) != 0


if __name__ == '__main__':
    BOOK_FILENAMES=['ivan_ilyich',
                         'cossacks',
                         'resurrection_p1',
                         'resurrection_p2',
                         'resurrection_p3',
                         ]
    for BOOK_FILENAME in BOOK_FILENAMES:
        print(get_book_frequency(BOOK_FILENAME))
