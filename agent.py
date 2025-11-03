# agent.py
from typing import Dict, Set, Tuple, Optional, List

class Agent:
    def __init__(self, prob_model, unigram_fallback: List[str]):
        """
        prob_model: instance of ProbabilisticModel (implements get_letter_probabilities(state))
        unigram_fallback: list of letters in descending freq order, uppercase (['E','A','R',...'])
        """
        self.model = prob_model
        self.unigram_fallback = [l.upper() for l in unigram_fallback]

    def choose_action(self, state: Tuple[str, Set[str], int]) -> str:
        """
        state: (masked_word_string, guessed_letters_set, remaining_lives)
               masked_word_string example: '_ P P L _' or '_____'
               guessed_letters_set: set of uppercase letters
        returns: a single uppercase letter not in guessed_letters_set
        """
        masked_word, guessed_set, _ = state
        # Ask probabilistic model for distribution
        prob_dist: Optional[Dict[str, float]] = None
        try:
            # ProbabilisticModel spec: get_letter_probabilities expects (masked_word, guessed_letters_set)
            prob_dist = self.model.get_letter_probabilities((masked_word, guessed_set))
        except Exception:
            prob_dist = None

        # If prob_dist is valid and non-empty, choose highest-prob letter not guessed
        if prob_dist:
            # Filter only letters not already guessed
            candidates = {l: p for l, p in prob_dist.items() if l not in guessed_set}
            if candidates:
                # Return letter with max probability
                best = max(candidates.items(), key=lambda x: x[1])[0]
                return best.upper()

        # Fallback: iterate unigram list and pick first not guessed
        for letter in self.unigram_fallback:
            if letter not in guessed_set:
                return letter

        # As a last resort (shouldn't happen), choose any letter A-Z not guessed
        import string
        for letter in string.ascii_uppercase:
            if letter not in guessed_set:
                return letter
        # If everything guessed, return 'A' (degenerate)
        return 'A'
