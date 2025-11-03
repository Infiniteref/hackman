# corpus.py
from collections import Counter
import string

def load_corpus(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return [w.strip().upper() for w in f if w.strip()]

def preprocess_corpus(corpus_list):
    d = {}
    for w in corpus_list:
        d.setdefault(len(w), set()).add(w)
    return d

def get_unigram_fallback(corpus_list):
    counter = Counter()
    for w in corpus_list:
        counter.update(list(w))
    letters = [c for c,_ in counter.most_common() if c in string.ascii_uppercase]
    return letters
