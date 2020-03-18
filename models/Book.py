class Book:
    def __init__(self, title, chapters, author=None, id=None):
        self.title = title
        self.chapters = chapters
        self.id = id
        if author is None:
            self.author = 'unknown'
        else:
            self.author = author