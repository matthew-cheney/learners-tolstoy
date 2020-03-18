import json

from models.Paragraph import Paragraph
from models.Word import Word
from models.Chapter import Chapter
from models.Book import Book


def dict_to_json(dict):
    return json.dumps(dict, ensure_ascii=False).encode('utf-8')

def json_to_dict(json_text):
    return json.loads(json_text)

def json_to_book(json_text):
    """
    Convert json_text to Book object hierarchy
    :param json_text: text in json format
    :return: Book object
    """
    try:
        json_dict = json.loads(json_text)
        chapters = list()
        for chapter in json_dict['chapters'].values():
            paragraphs = list()
            for paragraph in chapter['paragraphs'].values():
                words = list()
                for word in paragraph['words'].values():
                    # TO DO - Check if this is footnote for previous word
                    if word['text'].startswith('FOOTNOTE_ID'):
                        words[len(words) - 1].has_footnote = True
                        words[len(words) - 1].footnote_id = word['text'][12:]
                        words[len(words) - 1].footnote =\
                            json_dict['footnotes'][word['text'][12:]]
                        continue
                    # Not a footnote, add new word
                    new_word = Word(text=word['text'], lemma=word['lemma'],
                                    pos=word['pos'], feats=word['feats'],
                                    footnote=word['footnote'],
                                    footnote_id=word['footnote_id'],
                                    frequency=word['frequency'],
                                    translation=word['translation'])
                    words.append(new_word)
                paragraphs.append(Paragraph(words))
            chapters.append(Chapter(paragraphs=paragraphs, title=chapter['title'],
                                    number=chapter['number']))
        book = Book(title=json_dict['title'], chapters=chapters,
                    author=json_dict['author'])
        return book
    except json.decoder.JSONDecodeError:
        raise json.decoder.JSONDecodeError("json_text must be valid json")
    except IndexError:
        raise ValueError("most likely invalid parameter json_text")

def book_to_json(book: Book):
    chapters = dict()
    for chapter_index, chapter in enumerate(book.chapters):
        paragraphs = dict()
        for paragraph_index, paragraph in enumerate(chapter.paragraphs):
            words = dict()
            for word_index, word in enumerate(paragraph.words):
                word_dict = dict()
                word_dict['text'] = word.text
                word_dict['lemma'] = word.lemma
                word_dict['pos'] = word.pos
                word_dict['feats'] = word.feats
                word_dict['footnote'] = word.footnote
                word_dict['footnote_id'] = word.footnote_id
                word_dict['frequency'] = word.frequency
                word_dict['translation'] = word.translation
                words[f'{word_index:04d}'] = word_dict
            paragraphs[f'{paragraph_index:04d}'] = dict()
            paragraphs[f'{paragraph_index:04d}']['words'] = words
        chapter_dict = dict()
        chapter_dict['paragraphs'] = paragraphs
        chapter_dict['title'] = chapter.title
        chapter_dict['number'] = chapter_index
        chapters[f'{chapter_index:04d}'] = chapter_dict
    book_dict = dict()
    book_dict['title'] = book.title
    book_dict['author'] = book.author
    book_dict['chapters'] = chapters
    return dict_to_json(book_dict)

"""with open('../cleaned_pickles/ivan_ilyich_book.json', 'r') as f:
    raw_text = f.read()
book = json_to_book(raw_text)
book_json = book_to_json(book)
with open('test_json_ivan_ilyich.json', 'wb') as f:
    f.write(book_json)

with open('test_json_ivan_ilyich.json', 'r') as f:
    raw_text_2 = f.read()
book_2 = json_to_book(raw_text_2)

# Check if both books are equal
assert book.title == book_2.title
assert book.author == book_2.author
for i in range(len(book.chapters)):
    assert book.chapters[i].title == book_2.chapters[i].title
    assert book.chapters[i].number == book_2.chapters[i].number
    for j in range(len(book.chapters[i].paragraphs)):
        for k in range(len(book.chapters[i].paragraphs[j].words)):
            assert book.chapters[i].paragraphs[j].words[k].text == \
                   book_2.chapters[i].paragraphs[j].words[k].text
            assert book.chapters[i].paragraphs[j].words[k].lemma == \
                   book_2.chapters[i].paragraphs[j].words[k].lemma
            assert book.chapters[i].paragraphs[j].words[k].pos == \
                   book_2.chapters[i].paragraphs[j].words[k].pos
            assert book.chapters[i].paragraphs[j].words[k].feats == \
                   book_2.chapters[i].paragraphs[j].words[k].feats
            assert book.chapters[i].paragraphs[j].words[k].footnote == \
                   book_2.chapters[i].paragraphs[j].words[k].footnote
            assert book.chapters[i].paragraphs[j].words[k].footnote_id == \
                   book_2.chapters[i].paragraphs[j].words[k].footnote_id
            assert book.chapters[i].paragraphs[j].words[k].frequency == \
                   book_2.chapters[i].paragraphs[j].words[k].frequency
            assert book.chapters[i].paragraphs[j].words[k].translation == \
                   book_2.chapters[i].paragraphs[j].words[k].translation
x = 5"""