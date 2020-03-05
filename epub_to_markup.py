from epub_conversion.utils import open_book, convert_epub_to_lines
import glob
from tqdm import tqdm

filenames = glob.glob('tolstoy_ru/epubs/*.epub')

for filename in tqdm(filenames):
    book = open_book(filename)
    lines = convert_epub_to_lines(book)
    new_filename = f'{filename[-11:-5]}_markup.txt'
    with open(f'tolstoy_ru/markup/{new_filename}', 'w') as f:
        for line in lines:
            print(line, file=f)
