# corpus.py
from collections import Counter
from typing import Dict, Iterable, List, Set
import pickle
import os
import string

def load_corpus(filepath: str) -> List[str]:
    """
    Reads 'corpus.txt', converts words to uppercase, strips whitespace,
    and returns a list of words.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, "r", encoding="utf-8") as f:
        words = [w.strip().upper() for w in f if w.strip()]
    return words


def preprocess_corpus(corpus_list: Iterable[str]) -> Dict[int, Set[str]]:
    """
    Takes list of words and returns dict:
    {word_length: set(words_of_that_length)}
    Example: {5: {'APPLE', 'APPLY'}, 6: {'ORANGE', ...}}
    """
    result: Dict[int, Set[str]] = {}
    for word in corpus_list:
        L = len(word)
        if L > 0:
            result.setdefault(L, set()).add(word)
    return result


def get_unigram_fallback(corpus_list: Iterable[str]) -> List[str]:
    """
    Counts letter frequency across the corpus and returns a list
    of letters sorted from most to least frequent.
    """
    counter = Counter()
    for word in corpus_list:
        counter.update([ch for ch in word if ch.isalpha()])
    
    # Keep only A-Z uppercase
    letters = [c for c, _ in counter.most_common() if c in string.ascii_uppercase]
    return letters


# Optional helpers to cache preprocessed corpus
def save_preprocessed(preprocessed_dict, path="models/preprocessed.pkl"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(preprocessed_dict, f)


def load_preprocessed(path="models/preprocessed.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)
