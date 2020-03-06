class Word:

    def __init__(self, text, lemma, pos, feats, footnote=None,
                 footnote_id=None):
        self.text = text
        self.lemma = lemma
        self.pos = pos
        self.footnote = footnote
        self.footnote_id = footnote_id
        self.feats = feats
        self.has_footnote = (footnote is not None)
