"""
Probabilistic letter model for Hangman.

This module defines the ProbabilisticModel class which, given a preprocessed
corpus grouped by word length, filters candidate words based on the current
game state and returns a probability distribution over unguessed letters
appearing in any blank positions.

Assumptions:
- Masked characters are represented by "_" (underscore) in the masked_word.
- Words and guesses are treated in a case-insensitive manner; internally we
  normalize to uppercase.
"""

from __future__ import annotations

from collections import Counter
from typing import Dict, Optional, Sequence, Set, Tuple
import re


class ProbabilisticModel:
	"""Compute letter probabilities for Hangman based on a filtered corpus.

	Parameters
	----------
	processed_corpus_dict : Dict[int, Set[str]]
		Mapping from word length to a set (or sequence) of words of that length.
		Words are assumed to be alphabetic. Case-insensitive input is accepted
		and normalized to uppercase.

	Notes
	-----
	The main entry point is `get_letter_probabilities(state)` where `state` is a
	tuple of (masked_word, guessed_letters_set).
	"""

	BLANK_CHAR = "_"

	def __init__(self, processed_corpus_dict: Dict[int, Sequence[str]]):
		# Normalize all corpus words to uppercase and coerce to sets for fast membership.
		self.corpus_dict: Dict[int, Set[str]] = {}
		for length, words in processed_corpus_dict.items():
			# Defensive: allow any iterable of strings.
			normalized = {w.upper() for w in words if isinstance(w, str)}
			self.corpus_dict[int(length)] = normalized

	def get_letter_probabilities(
		self, state: Tuple[str, Set[str]]
	) -> Optional[Dict[str, float]]:
		"""Return probabilities over unguessed letters given game state.

		Parameters
		----------
		state : Tuple[str, Set[str]]
			A tuple of (masked_word, guessed_letters_set). The masked_word uses
			'_' to indicate unknown letters, and concrete letters for known
			positions. guessed_letters_set contains all letters that have been
			guessed so far (both correct and incorrect).

		Returns
		-------
		Optional[Dict[str, float]]
			A dictionary mapping each unguessed letter (A-Z) to its probability
			of appearing in any of the blank positions across all valid
			candidate words. Returns None if no valid candidate words remain.
		"""

		masked_word, guessed_letters = state
		if masked_word is None:
			return None

		# Normalize to uppercase to ensure consistent comparisons.
		masked_word = masked_word.upper()
		guessed_letters = {c.upper() for c in (guessed_letters or set())}

		length = len(masked_word)
		potential_words = self.corpus_dict.get(length, set())
		if not potential_words:
			return None

		# Build regex replacing blanks with '.' and anchoring to full match.
		# Non-blank characters are treated literally. Assume only A-Z and '_' appear.
		# Example: _PPL_ -> ^.PPL.$
		regex_pattern = "^" + re.escape(masked_word).replace(re.escape(self.BLANK_CHAR), ".") + "$"
		pattern = re.compile(regex_pattern)

		# 1) Regex filter
		regex_matches = [w for w in potential_words if pattern.match(w)]
		if not regex_matches:
			return None

		# 2) Remove words containing letters that have been guessed but are NOT in the masked pattern
		#    (i.e., previously guessed wrong letters)
		revealed_letters = set(ch for ch in masked_word if ch != self.BLANK_CHAR)
		invalid_letters = guessed_letters - revealed_letters

		if invalid_letters:
			invalid_re = re.compile("[" + "".join(sorted(invalid_letters)) + "]")
			valid_words = [w for w in regex_matches if not invalid_re.search(w)]
		else:
			valid_words = regex_matches

		if not valid_words:
			return None

		# 3) Count letter frequencies ONLY in blank positions across valid words.
		blank_positions = [i for i, ch in enumerate(masked_word) if ch == self.BLANK_CHAR]
		if not blank_positions:
			# No blanks left; nothing to predict.
			return {}

		counts: Counter[str] = Counter()
		for w in valid_words:
			for i in blank_positions:
				ch = w[i]
				counts[ch] += 1

		# Exclude letters that have already been guessed from probability candidates.
		for g in guessed_letters:
			if g in counts:
				del counts[g]

		total = sum(counts.values())
		if total == 0:
			return {}

		probs = {ch: counts[ch] / total for ch in counts}
		# Sort not required by spec, but stable order can help downstream.
		# Return as-is; callers can sort if needed.
		return probs


__all__ = ["ProbabilisticModel"]

