import json

from bs4 import BeautifulSoup
import pickle
import stanfordnlp

from models.Book import Book
from models.Chapter import Chapter
from models.Paragraph import Paragraph
from models.Word import Word

AUTHOR = 'Tolstoy'

nlp = stanfordnlp.Pipeline(lang='ru')

with open('tolstoy_ru/cleaned_markup/ivan_ilyich.txt', 'r') as f:
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
for link in link_divs:
    footnotes[link.get('id')] = link.find('p').text

# Build each Chapter model
chapters = {}
for chapter_number, chapter in enumerate(chapter_list):
    paragraphs = {}
    for paragraph_index, paragraph in enumerate(chapter.findAll('p')):
        # TO DO - change to CoreNLP word tokenizing
        raw_paragraph_text = paragraph.text
        words = {}
        doc = nlp(paragraph.text)
        word_counter = 0
        for sentence_index, sentence in enumerate(doc.sentences):
            for word_index, word in enumerate(sentence.words):
                word_dict = dict()
                word_dict['text'] = word.text
                word_dict['lemma'] = word.lemma
                word_dict['pos'] = word.upos
                word_dict['feats'] = word.feats
                words[f'{word_counter:04d}'] = word_dict
                word_counter += 1
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

with open('cleaned_pickles/ivan_ilyich_book.json', 'wb') as f:
    f.write(json_dict)
