class Word:

    def __init__(self, text, lemma, pos, feats, footnote=None):
        self.text = text
        self.lemma = lemma
        self.pos = pos
        self.footnote = footnote
        self.feats = feats
        self.has_footnote = (footnote is not None)
