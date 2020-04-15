class Paragraph:
    def __init__(self, words):
        self.words = words

    def get_text(self):
        text_list = []
        for word in self.words:
            text_list.append(word.text)
        return text_list

    def get_lemmas(self):
        text_list = []
        for word in self.words:
            text_list.append(word.lemma)
        return text_list
