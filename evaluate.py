# evaluate.py
import os
from corpus import load_corpus, preprocess_corpus, get_unigram_fallback
from hangman_env import HangmanEnv
from prob_model import ProbabilisticModel
from agent import Agent

def load_test_set(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [w.strip().upper() for w in f if w.strip()]

def main(corpus_path='corpus.txt', test_path='test.txt', max_lives=6, verbose=False):
    # 1. load corpus
    corpus_list = load_corpus(corpus_path)  # returns uppercase list
    corpus_dict = preprocess_corpus(corpus_list)  # {length: set(words)}
    unigram = get_unigram_fallback(corpus_list)  # ['E','A',...]
    # 2. instantiate model and agent
    prob_model = ProbabilisticModel(corpus_dict)
    agent = Agent(prob_model, unigram)

    # 3. load test set
    test_words = load_test_set(test_path)

    # 4. counters
    total_wins = 0
    total_wrong_guesses = 0
    total_repeated_guesses = 0

    # 5. run
    for i, word in enumerate(test_words, 1):
        env = HangmanEnv(word, lives=max_lives)
        done = False
        info = {}
        while not done:
            state = env.get_state()  # (masked_word, guessed_set, remaining_lives)
            action = agent.choose_action(state)
            new_state, done, info = env.step(action)
            # info parsing:
            if info.get('is_repeat'):
                total_repeated_guesses += 1
            elif info.get('status') == 'wrong':
                total_wrong_guesses += 1
        if info.get('status') == 'win':
            total_wins += 1

        if verbose and i % 50 == 0:
            print(f"Processed {i}/{len(test_words)}. Wins: {total_wins}")

    # 6. metrics
    success_rate = total_wins / len(test_words)
    final_score = (success_rate * 2000) - (total_wrong_guesses * 5) - (total_repeated_guesses * 2)

    print("=== Results ===")
    print(f"Total Games: {len(test_words)}")
    print(f"Success Rate: {success_rate:.4f} ({total_wins} wins)")
    print(f"Total Wrong Guesses: {total_wrong_guesses}")
    print(f"Total Repeated Guesses: {total_repeated_guesses}")
    print(f"Final Score: {final_score:.2f}")

if __name__ == "__main__":
    main(verbose=True)