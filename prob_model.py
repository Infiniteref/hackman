# prob_model.py -- cleaned version

import re
from collections import Counter
from typing import Dict, Set, Tuple, Optional

class ProbabilisticModel:
    """
    Probabilistic filter that returns a probability distribution over unguessed letters
    given (masked_word, guessed_set, remaining_lives).
    Uses position-wise frequencies + unigram fallback with smoothing.
    """
    def __init__(self, corpus_dict):
        # corpus_dict: {length: set(words)} with words in UPPERCASE
        self.corpus = corpus_dict

        # Precompute unigram frequencies across entire corpus for fallback
        all_letters = Counter()
        for words in corpus_dict.values():
            for w in words:
                all_letters.update(w)
        self.unigram_counts = dict(all_letters)
        self.unigram_total = sum(self.unigram_counts.values()) or 1

        # Precompute position counts per length
        self.position_counts = {}
        for L, words in corpus_dict.items():
            pos_counts = [Counter() for _ in range(L)]
            for w in words:
                for i, ch in enumerate(w):
                    pos_counts[i][ch] += 1
            self.position_counts[L] = pos_counts

    def _position_score(self, blanks: list, candidates: list) -> Counter:
        counts = Counter()
        for w in candidates:
            for i in blanks:
                counts[w[i]] += 1
        return counts

    def _positional_backoff_probs(self, length: int, blanks: list, candidates: list, guessed_set: Set[str]):
        pos_counts = self._position_score(blanks, candidates)
        total_pos = sum(pos_counts.values())

        alpha = 1.0
        import string
        letters = list(string.ascii_uppercase)
        V = 26

        probs = {}
        for L in letters:
            p_pos = (pos_counts.get(L, 0) + alpha) / (total_pos + alpha * V)
            p_uni = (self.unigram_counts.get(L, 0) + alpha) / (self.unigram_total + alpha * V)
            probs[L] = 0.75 * p_pos + 0.25 * p_uni

        for g in guessed_set:
            probs.pop(g, None)

        s = sum(probs.values()) or 1.0
        for k in list(probs.keys()):
            probs[k] = probs[k] / s

        return probs

    def get_letter_probabilities(self, state: Tuple[str, Set[str], int]) -> Optional[Dict[str, float]]:
        # Accept either (masked, guessed_set, lives) or (masked, guessed_set)
        if len(state) == 3:
            masked_word, guessed_set, _ = state
        else:
            masked_word, guessed_set = state

        masked = masked_word.replace(' ', '').upper()
        L = len(masked)
        candidates = list(self.corpus.get(L, set()))
        if not candidates:
            return None

        pattern = '^' + ''.join('.' if ch == '_' else ch for ch in masked) + '$'
        regex = re.compile(pattern)
        matches = [w for w in candidates if regex.match(w)]
        if not matches:
            matches = candidates

        invalids = {g for g in guessed_set if g not in set(masked)}
        filtered = [w for w in matches if not any(ch in invalids for ch in w)]
        if not filtered:
            filtered = matches
            if not filtered:
                return None

        blanks = [i for i, ch in enumerate(masked) if ch == '_']
        if not blanks:
            return None

        probs = self._positional_backoff_probs(L, blanks, filtered, guessed_set)
        return probs
