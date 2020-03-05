class Book:
    def __init__(self, title, chapters, author=None):
        self.title = title
        self.chapters = chapters
        if author is None:
            self.author = 'unknown'
        else:
            self.author = author