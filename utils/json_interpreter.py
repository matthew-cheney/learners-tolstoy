import json

from models.Paragraph import Paragraph
from models.Word import Word
from models.Chapter import Chapter
from models.Book import Book


def dict_to_json(dict):
    return json.dumps(dict, ensure_ascii=False).encode('utf-8')

def json_to_dict(json_text):
    return json.loads(json_text)

def json_to_book_footnotes_separate(json_text):
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
                    if word['text'].startswith('FOOTNOTE_ID_'):
                        words[len(words) - 1].has_footnote = True
                        words[len(words) - 1].footnote_id = word['text'][12:]
                        f_words = list()
                        for f_word in json_dict['footnotes'][word['text'][12:]]['words'].values():
                            new_ft_word = Word(text=f_word['text'],
                                            lemma=f_word['lemma'],
                                            pos=f_word['pos'],
                                            feats=f_word['feats'],
                                            footnote=f_word['footnote'],
                                            footnote_id=f_word['footnote_id'],
                                            frequency=f_word['frequency'],
                                            translation=f_word['translation'])
                            f_words.append(new_ft_word)
                        words[len(words) - 1].footnote = f_words
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
                    # Not a footnote, add new word
                    new_word = Word(text=word['text'], lemma=word['lemma'],
                                    pos=word['pos'], feats=word['feats'],
                                    frequency=word['frequency'],
                                    translation=word['translation'])
                    if word['footnote_id'] != None:
                        new_word.footnote_id = word['footnote_id']
                        f_words = list()
                        for f_word in word['footnote'].values():
                            new_ft_word = Word(text=f_word['text'],
                                               lemma=f_word['lemma'],
                                               pos=f_word['pos'],
                                               feats=f_word['feats'],
                                               footnote=f_word['footnote'],
                                               footnote_id=f_word[
                                                   'footnote_id'],
                                               frequency=f_word['frequency'],
                                               translation=f_word[
                                                   'translation'])
                            f_words.append(new_ft_word)
                        new_word.footnote = f_words
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
                if chapter_index == 1 and paragraph_index == 3 and word_index == 100:
                    stop_here = True
                    pass
                if isinstance(word.footnote, list):
                    ft_dict = dict()
                    for ft_word_index, ft_word in enumerate(word.footnote):
                        ft_word_dict = dict()
                        ft_word_dict['text'] = ft_word.text
                        ft_word_dict['lemma'] = ft_word.lemma
                        ft_word_dict['pos'] = ft_word.pos
                        ft_word_dict['feats'] = ft_word.feats
                        ft_word_dict['footnote'] = ft_word.footnote
                        ft_word_dict['footnote_id'] = ft_word.footnote_id
                        ft_word_dict['frequency'] = ft_word.frequency
                        ft_word_dict['translation'] = ft_word.translation
                        ft_dict[ft_word_index] = ft_word_dict
                    word_dict['footnote'] = ft_dict
                else:
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

"""with open('../cleaned_pickles/ivan_ilyich_book_with_translations.json', 'r') as f:
    raw_text = f.read()
book = json_to_book(raw_text)
x = 0

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