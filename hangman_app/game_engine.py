import random
from typing import Tuple


class HangmanGame:
    def __init__(self):
        self.max_wrong_guesses = 6
        self.max_total_guesses = 10

    def random_word(self, words: list[str]) -> str:
        word = random.choice(words)
        return word.upper()

    def display_word(self, used_letters: list[str] = [], word: str = "") -> str:
        revealed_word = ""
        for char in word:
            if char in used_letters:
                revealed_word += char + " "
            else:
                revealed_word += "_ "
        return revealed_word.strip()

    def check_guessed_letter(
        self, revealed_letter: str, word: str, wrong_guesses: int
    ) -> Tuple[bool, int]:
        unique_word_letters = set(word)
        if revealed_letter not in unique_word_letters:
            wrong_guesses += 1
            return False, wrong_guesses
        else:
            return True, wrong_guesses

    def check_word(self, guessed_word: str, word: str):
        if guessed_word.upper() == word:
            return True
        else:
            return False

    def check_total_guesses(self, total_guesses: int) -> bool:
        if total_guesses >= self.max_total_guesses:
            return True
        else:
            return False

    def check_is_word_already_guessed(
        self, revealed_letters: list[str], word: str
    ) -> bool:
        unique_word_letters = set(word)
        if all(letter in revealed_letters for letter in unique_word_letters):
            return True
        else:
            return False

    def check_max_errors(self, wrong_guesses: int):
        if wrong_guesses >= self.max_wrong_guesses:
            return True
        else:
            False
