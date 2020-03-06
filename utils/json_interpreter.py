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
                        words[len(words) - 1].footnote_id = word['text'][9:]
                        continue
                    # Not a footnote, add new word
                    new_word = Word(text=word['text'], lemma=word['lemma'],
                                    pos=word['pos'], feats=word['feats'])
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
    return json_dict

with open('../cleaned_pickles/ivan_ilyich_book.json', 'r') as f:
    raw_text = f.read()
book = json_to_book(raw_text)
x = 5