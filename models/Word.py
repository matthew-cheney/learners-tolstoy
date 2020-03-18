import uuid

class Word:

    def __init__(self, text, lemma, pos, feats, footnote=None,
                 footnote_id=None, frequency=None, translation=None):
        self.id = uuid.uuid4().hex
        self.text = text
        self.lemma = lemma
        self.pos = pos
        self.footnote = footnote
        self.footnote_id = footnote_id
        self.feats = feats
        self.has_footnote = (footnote is not None)
        if frequency is None:
            self.frequency = float('infinity')
        else:
            self.frequency = frequency
        self.translation = translation