import kenlm

from utils.json_interpreter import json_to_book


def analyze_probs(BOOK_FILENAME):
    """
    Generate a csv with MWE probabilities and perplexity
    :param BOOK_FILENAME: filename (not entire path) of target book (with translations)
    :return: Nothing. Creates csv file in kenlm/csvs directory
    """


    SLICE_SIZE = 3

    # Load language model
    model = kenlm.Model("arpas/tolstoy_small_lemmas.mmap")

    # Get book loaded as object

    with open(f'../cleaned_json/{BOOK_FILENAME}_book_with_translations.json', 'r') as f:
        raw_text = f.read()
    book = json_to_book(raw_text)

    with open(f'csvs/{BOOK_FILENAME}_mwe.csv', 'w') as f:
        print('text,score,perplexity', file=f)
        for ci, chapter in enumerate(book.chapters):
            print(f'processing chapter {ci} / {len(book.chapters)}')
            for paragraph in chapter.paragraphs:
                word_list = paragraph.get_lemmas()
                if len(word_list) < SLICE_SIZE:
                    continue
                i = 0
                j = SLICE_SIZE
                while j < len(word_list):
                    try:
                        input_text = ' '.join(word_list[i:j])
                    except TypeError:
                        i += 1
                        j += 1
                        continue
                    print(f'"{input_text}"', model.score(input_text),
                          model.perplexity(input_text), sep=',', file=f)
                    i += 1
                    j += 1


if __name__ == '__main__':
    from sys import argv
    if len(argv) < 2:
        print(f'USAGE: {argv[0]} <filename (not path)>')
        exit(1)
    analyze_probs(argv[1])
