class Chapter:
    def __init__(self, paragraphs, title=None, number=None):
        self.paragraphs = paragraphs
        if title is None:
            self.title = 'none'
        else:
            self.title = title
        if number is None:
            self.number = 'none'
        else:
            self.number = number