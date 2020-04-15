import json
import re

from bs4 import BeautifulSoup
import stanfordnlp


import warnings

warnings.filterwarnings("ignore")

AUTHOR = 'Leo Tolstoy'


def markup_to_json(BOOK_FILENAME):
    nlp = stanfordnlp.Pipeline(lang='ru')

    print(f'processing book {BOOK_FILENAME}')

    with open(f'tolstoy_ru/cleaned_markup/{BOOK_FILENAME}.txt', 'r') as f:
        raw_text = f.read()

    soup = BeautifulSoup(raw_text, 'html.parser')

    # Get the title
    title_div = soup.find('div', {'class': 'title'})
    title_header = title_div.find('h2')

    # Get the chapters
    chapter_list = soup.findAll('div', {'class': 'chapter'})

    # Get the footnotes
    links_wrapper = soup.find('div', {'class': 'links'})
    link_divs = links_wrapper.findAll('div', {'class': 'link'})

    # Put footnotes into dictionary
    # keys: id (str); values: <p>Transl. (bs4 Tag)
    footnotes = dict()
    print('parsing links/footnotes')
    for link in link_divs:
        f_doc = nlp(link.find('p').text)
        f_words = {}
        word_counter = 0
        for sentence_index, sentence in enumerate(f_doc.sentences):
            for word_index, word in enumerate(sentence.words):
                word_dict = dict()
                word_dict['text'] = word.text
                word_dict['lemma'] = word.lemma
                word_dict['pos'] = word.upos
                word_dict['feats'] = word.feats
                word_dict['footnote'] = None
                word_dict['footnote_id'] = None
                word_dict['frequency'] = float('infinity')
                word_dict['translation'] = None
                f_words[f'{word_counter:04d}'] = word_dict
                word_counter += 1
        footnotes[link.get('id')] = dict()
        footnotes[link.get('id')]['words'] = f_words

    from pprint import pprint

    # Build each Chapter model
    chapters = {}
    footnotes_caught = 0
    for chapter_number, chapter in enumerate(chapter_list):
        # if chapter_number > 3:
        #     continue
        print(f'\nstarting to parse chapter {chapter_number+1} / {len(chapter_list)}')
        paragraphs = {}
        paragraph_list = chapter.findAll('p')
        for paragraph_index, paragraph in enumerate(chapter.findAll('p')):
            raw_paragraph_text = paragraph.text
            words = {}
            paragraph_footnotes = re.findall(r'(.*?)(FOOTNOTE_ID_[0-9]*)', raw_paragraph_text)
            if len(paragraph_footnotes) > 0:
                xtmp = 0
            # if len(paragraph_footnotes) > 0:
            #     pprint(paragraph_footnotes)
            footnotes_caught += len(paragraph_footnotes)
            text_without_footnotes = raw_paragraph_text
            for each in paragraph_footnotes:
                text_without_footnotes = text_without_footnotes.replace(each[1], '')
            for i in range(len(paragraph_footnotes)):
                paragraph_footnotes[i] = (paragraph_footnotes[i][0].replace(' ', ''), paragraph_footnotes[i][1])
            if text_without_footnotes.strip() == '':
                continue
            doc = nlp(text_without_footnotes)
            word_counter = 0
            text_so_far = ''
            footnote_counter = 0
            for sentence_index, sentence in enumerate(doc.sentences):
                for word_index, word in enumerate(sentence.words):
                    try:
                        footnote_found = paragraph_footnotes[footnote_counter][0] == text_so_far
                    except IndexError:
                        footnote_found = False
                    if footnote_found:
                        word_dict = dict()
                        word_dict['text'] = paragraph_footnotes[footnote_counter][1]
                        word_dict['lemma'] = paragraph_footnotes[footnote_counter][1]
                        word_dict['pos'] = 'footnote'
                        word_dict['feats'] = 'footnote'
                        word_dict['footnote'] = None
                        word_dict['footnote_id'] = None
                        word_dict['frequency'] = float('infinity')
                        word_dict['translation'] = None
                        words[f'{word_counter:04d}'] = word_dict
                        word_counter += 1
                        text_so_far = ''
                        footnote_counter += 1

                    word_dict = dict()
                    word_dict['text'] = word.text
                    word_dict['lemma'] = word.lemma
                    word_dict['pos'] = word.upos
                    word_dict['feats'] = word.feats
                    word_dict['footnote'] = None
                    word_dict['footnote_id'] = None
                    word_dict['frequency'] = float('infinity')
                    word_dict['translation'] = None
                    words[f'{word_counter:04d}'] = word_dict
                    word_counter += 1
                    text_so_far += word.text
                try:
                    footnote_found = paragraph_footnotes[footnote_counter][
                                         0] == text_so_far
                except IndexError:
                    footnote_found = False
                if footnote_found:
                    word_dict = dict()
                    word_dict['text'] = paragraph_footnotes[footnote_counter][1]
                    word_dict['lemma'] = paragraph_footnotes[footnote_counter][1]
                    word_dict['pos'] = 'footnote'
                    word_dict['feats'] = 'footnote'
                    word_dict['footnote'] = None
                    word_dict['footnote_id'] = None
                    word_dict['frequency'] = float('infinity')
                    word_dict['translation'] = None
                    words[f'{word_counter:04d}'] = word_dict
                    word_counter += 1
                    text_so_far = ''
                    footnote_counter += 1
            paragraphs[f'{paragraph_index:04d}'] = dict()
            paragraphs[f'{paragraph_index:04d}']['words'] = words
        chapter_dict = dict()
        chapter_dict['paragraphs'] = paragraphs
        chapter_dict['title'] = chapter.find('h3', {'class': 'chapter_title'}).text
        chapter_dict['number'] = chapter_number
        chapters[f'{chapter_number:04d}'] = chapter_dict

    # Store book in JSON

    book_dict = dict()

    book_dict['title'] = title_header.text
    book_dict['author'] = AUTHOR
    book_dict['chapters'] = chapters

    # Add in footnotes (at end of json, not integrated with words)
    book_dict['footnotes'] = footnotes

    json_dict = json.dumps(book_dict, ensure_ascii=False).encode('utf-8')

    with open(f'cleaned_pickles/{BOOK_FILENAME}_book.json', 'wb') as f:
        f.write(json_dict)

    print(f'{footnotes_caught} footnotes caught')

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
        print(f'processing {BOOK_FILENAME}')
        markup_to_json(BOOK_FILENAME)

"""
if __name__ == '__main__':
    from sys import argv
    if len(argv) < 2:
        print(f'USAGE: {argv[0]} <filename (not path)>')
        exit(1)
    markup_to_json(argv[1])
"""