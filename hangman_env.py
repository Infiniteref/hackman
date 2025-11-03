# hangman_env.py

class HangmanEnv:
    def __init__(self, word, lives=6):
        """
        Initialize a new Hangman environment.
        """
        self.word = word.upper()
        self.lives = lives
        self.guessed = set()

    def get_state(self):
        """
        Returns current game state as (masked_word, guessed_letters, remaining_lives)
        """
        masked = ''.join(ch if ch in self.guessed else '_' for ch in self.word)
        return (masked, set(self.guessed), self.lives)

    def reset(self):
        """
        Reset the game to its initial state.
        """
        self.guessed = set()
        self.lives = 6
        return self.get_state()

    def step(self, letter):
        """
        Process a letter guess and return (new_state, done, info_dict).
        info_dict contains status: 'correct', 'wrong', 'repeat', 'win', 'lose'
        """
        letter = letter.upper()

        # If repeated guess
        if letter in self.guessed:
            return self.get_state(), False, {'status': 'repeat', 'is_repeat': True}

        # Add to guessed letters
        self.guessed.add(letter)

        # Correct guess
        if letter in self.word:
            if all(ch in self.guessed for ch in self.word):
                # All letters guessed → Win
                return self.get_state(), True, {'status': 'win', 'is_repeat': False}
            return self.get_state(), False, {'status': 'correct', 'is_repeat': False}

        # Wrong guess
        else:
            self.lives -= 1
            if self.lives <= 0:
                return self.get_state(), True, {'status': 'lose', 'is_repeat': False}
            return self.get_state(), False, {'status': 'wrong', 'is_repeat': False}
