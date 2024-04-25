import unittest
from game_engine import HangmanGame


class TestHangmanGame(unittest.TestCase):
    def setUp(self):
        self.game = HangmanGame()

    def test_random_word(self):
        words = ["APPLE", "BANANA", "ORANGE"]
        random_word = self.game.random_word(words)
        self.assertIn(random_word, words)

    def test_display_word(self):
        used_letters = ["A", "E", "I"]
        word = "APPLE"
        displayed_word = self.game.display_word(used_letters, word)
        self.assertEqual(displayed_word, "A _ _ _ E")

    def test_check_guessed_letter_correct(self):
        revealed_letter = "A"
        word = "APPLE"
        wrong_guesses = 0
        is_correct, new_wrong_guesses = self.game.check_guessed_letter(
            revealed_letter, word, wrong_guesses
        )
        self.assertTrue(is_correct)
        self.assertEqual(new_wrong_guesses, 0)

    def test_check_guessed_letter_incorrect(self):
        revealed_letter = "Z"
        word = "APPLE"
        wrong_guesses = 0
        is_correct, new_wrong_guesses = self.game.check_guessed_letter(
            revealed_letter, word, wrong_guesses
        )
        self.assertFalse(is_correct)
        self.assertEqual(new_wrong_guesses, 1)

    def test_check_word_correct(self):
        guessed_word = "APPLE"
        word = "APPLE"
        result = self.game.check_word(guessed_word, word)
        self.assertTrue(result)

    def test_check_word_incorrect(self):
        guessed_word = "ORANGE"
        word = "APPLE"
        result = self.game.check_word(guessed_word, word)
        self.assertFalse(result)

    def test_check_total_guesses_true(self):
        total_guesses = 11
        result, _ = self.game.check_total_guesses(total_guesses)
        self.assertTrue(result)

    def test_check_total_guesses_false(self):
        total_guesses = 9
        result, _ = self.game.check_total_guesses(total_guesses)
        self.assertFalse(result)

    def test_check_is_word_already_guessed_true(self):
        revealed_letters = ["A", "P", "L", "E"]
        word = "APPLE"
        result = self.game.check_is_word_already_guessed(revealed_letters, word)
        self.assertTrue(result)

    def test_check_is_word_already_guessed_false(self):
        revealed_letters = ["A", "P"]
        word = "APPLE"
        result = self.game.check_is_word_already_guessed(revealed_letters, word)
        self.assertFalse(result)

    def test_check_max_errors_true(self):
        wrong_guesses = 6
        result = self.game.check_max_errors(wrong_guesses)
        self.assertTrue(result)

    def test_check_max_errors_false(self):
        wrong_guesses = 4
        result = self.game.check_max_errors(wrong_guesses)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
