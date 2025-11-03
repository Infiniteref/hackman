# corpus.py
from collections import Counter
from typing import Dict, Iterable, List, Set
import pickle, os

def load_corpus(filepath: str) -> List[str]:
    """
    Reads 'corpus.txt', converts words to uppercase, strips whitespace,
    and returns a list of words.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    words: List[str] = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            w = line.strip()
            if w:
                words.append(w.upper())
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
        if L == 0:
            continue
        result.setdefault(L, set()).add(word)
    return result


def get_unigram_fallback(corpus_list: Iterable[str]) -> List[str]:
    """
    Counts letter frequency across the corpus.
    Returns list of letters sorted by descending frequency.
    """
    counter = Counter()
    for word in corpus_list:
        for ch in word:
            if ch.isalpha():
                counter[ch.upper()] += 1
    sorted_letters = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
    return [letter for letter, _ in sorted_letters]


# (optional helper to cache preprocessed corpus)
def save_preprocessed(preprocessed_dict, path="models/preprocessed.pkl"):
    with open(path, "wb") as f:
        pickle.dump(preprocessed_dict, f)

def load_preprocessed(path="models/preprocessed.pkl"):
    with open(path, "rb") as f:
        return pickle.load(f)
