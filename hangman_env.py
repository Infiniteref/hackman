# hangman_env.py

class HangmanEnv:
    """
    The Environment Architect's job: a perfect, bug-free simulation 
    of the Hangman game environment.
    """
    def __init__(self, word: str, lives: int = 6):
        """Initializes the game with a secret word and starting lives."""
        self.secret_word = str(word).upper()
        self.initial_lives = int(lives)
        self.reset()

    def _get_masked_word(self) -> str:
        """Helper function: Returns the current state of the word with unguessed letters masked."""
        masked = ""
        for letter in self.secret_word:
            masked += letter if letter in self.guessed_letters else '_'
        return masked

    def _is_win(self) -> bool:
        """Helper function: Checks if the game has been won (all letters revealed)."""
        return '_' not in self._get_masked_word()

    def reset(self):
        """Resets the game to the starting state."""
        self.guessed_letters = set()
        self.remaining_lives = self.initial_lives
        # Return the initial state tuple
        return self.get_state()

    def get_state(self) -> tuple:
        """
        Returns the current state as a tuple, following the agreed-upon definition:
        state = (masked_word, guessed_letters_set, remaining_lives)
        """
        return (self._get_masked_word(), self.guessed_letters.copy(), self.remaining_lives)

    def step(self, letter: str) -> tuple:
        """
        Processes a single letter guess.

        Returns a tuple: (new_state, done, info_dict)
        """
        if not letter:
            return self.get_state(), False, {'status': 'repeat', 'is_repeat': True}

        letter = str(letter).upper()

        # Initialize return values
        done = False
        info_dict = {'status': 'new_guess', 'is_repeat': False}

        # 1. Handle repeated guess
        if letter in self.guessed_letters:
            info_dict = {'status': 'repeat', 'is_repeat': True}
            return (self.get_state(), done, info_dict)

        # Mark letter as guessed
        self.guessed_letters.add(letter)

        # 2. Handle correct or incorrect new guess
        if letter in self.secret_word:
            # correct guess
            if self._is_win():
                done = True
                info_dict = {'status': 'win', 'is_repeat': False}
            else:
                info_dict = {'status': 'correct', 'is_repeat': False}
        else:
            # wrong guess
            self.remaining_lives -= 1
            if self.remaining_lives <= 0:
                done = True
                info_dict = {'status': 'lose', 'is_repeat': False}
            else:
                info_dict = {'status': 'wrong', 'is_repeat': False}

        return (self.get_state(), done, info_dict)
