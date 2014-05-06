#!/usr/bin/env python
import re
import collections.defaultdict as defaultdict
import pdb
import heapq
import pickle
import os.path


def words(text):
    return re.findall('[a-z]+', text.lower())


def train(features):
    if(os.path.isfile('dict.p')):
        return pickle.load(open('dict.p', 'rb'))
    model = defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    pdb.set_trace()
    pickle.dump(model.items(), open('dict.p', 'wb'))
    return model

NWORDS = train(words(open('big.txt', 'r').read()))
alphabet = 'abcdefghijklmnopqrstuvwxyz'


def edits1(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts = [a + c + b for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)


def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)


def known(words):
    return set(w for w in words if w in NWORDS)


def correct(word):
    candidates = known([word]) or known(edits1(word))
    candidates = candidates or known_edits2(word) or [word]
    print(heapq.nlargest(10, candidates, key=NWORDS.get))
    return max(candidates, key=NWORDS.get)


def main():
    while(True):
        word_to_correct = input("Enter a word to correct: ")
        print(correct(word_to_correct))


if __name__ == '__main__':
    main()
