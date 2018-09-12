#!/usr/bin/env python3

from collections import defaultdict, namedtuple, Counter
from operator import attrgetter

from nltk.stem.porter import PorterStemmer as _PorterStemmer

_RevToken = namedtuple('RevToken', ['unit', 'orig'])


class RevToken(_RevToken):
    def __str__(self):
        return str(self.unit)

class PorterStemmer(_PorterStemmer):
    '''
    Extends nltk.stem.porter.PorterStemmer as a vocabulary aware
    reverse stemmer. This tool is used to increase interpretability
    by mantianing a human vocabulary after stemming
    '''
    def __init__(self, truncable, blacklist, protected=set(),
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._lookup = defaultdict(Counter)
        self._vocabulary = set(truncable)
        self._stopwords = set(blacklist)
        self._protected = set(protected)

    def _stem_token(self, word, *args, **kwargs):
        if word in self._stopwords:
            return None

        if word not in self._vocabulary or word in self._protected:
            token = RevToken(word, word)
        else:
            s = super().stem(word, *args, **kwargs)
            token = RevToken(s, word)
        return token

    def stem(self, word, *args, **kwargs):
        '''
        stem if applicable and drop stopwords

        returns reversable token or None

        (applies, applying, apply) -> (appli)
        (<stopword>) -> None
        '''
        token = self._stem_token(word, *args, **kwargs)
        if token is not None:
            self._lookup[token.unit].update([token.orig])
        return token

    def stem_unstem(self, word, *args, **kwargs):
        '''
        atomic stem then unstem apply
        requires stemmer to have already been populated

        returns reversable token or None

        (applies, applying, apply) -> (appli) -> (apply)
        '''
        token = self._stem_token(word, *args, **kwargs)
        if token:
            return self.best_unstem(token.unit)
        else:
            return token

    def get_words(self, stem):
        if isinstance(stem, RevToken):
            idx = stem.unit
        else: # stem is a string
            idx = stem

        assert(isinstance(idx, str)), type(idx)
        return self._lookup[idx]

    def rare_stems(self, occurances=1, ignored=[]):
        rare = [idx for idx in self._lookup
                if len(self._lookup[idx]) <= occurances]
        return [idx for idx in rare if idx not in ignored]

    @property
    def vocabulary(self):
        return {idx for idx in self._lookup}

    def best_unstem(self, key):
        '''
        unstem previously stemmed word

        requires stemmer to have already been populated

        (appli) -> (apply)
        '''
        return self._lookup[key].most_common()[0][0]

    def _apply_document(self, stemtype, document):
        apply_doc = [
            x
            for x in map(attrgetter(stemtype)(self), document.split())
            if x
        ]
        return apply_doc

    def stem_document(self, document):
        '''
        stem a whiltespace seperated document, and update stemmer dictionary
        '''
        return ' '.join(x.unit for x in self._apply_document('stem', document))

    def unstem_document(self, document):
        '''
        unstem a whiltespace seperated document from an updated stemmer dictionary
        '''
        return ' '.join(x for x in self._apply_document('best_unstem', document))

    def stem_unstem_document(self, document):
        '''
        stem then unstem a whiltespace seperated document from an updated stemmer dictionary
        '''
        return ' '.join(x for x in self._apply_document('stem_unstem', document))


def test():

    pstemmer = PorterStemmer()
    print(pstemmer.stem('running'))
    print(pstemmer.stem('runs'))
    print(pstemmer.stem('ran'))
    print(pstemmer.stem('the'))
    print(pstemmer._lookup)
    print(*pstemmer.vocabulary)


if __name__ == '__main__':
    test()
