from functools import wraps
import random

class Word:
    def __init__(self):
        self.word = self.random_word()

    def random_word(self) -> str:
        try:
            with open("words.txt", "r") as data:
                words_list = data.read().splitlines()
            word = random.choice(words_list)
            return word.lower()
        except FileNotFoundError:
            print("Error: File 'words.txt' not found.")
            exit(1)
        except Exception as error:
            print(f"Error: {error}")
            exit(1)

    def display_word(self, used_letters: list) -> None:
        revealed_word = ""
        for char in self.word:
            if char in used_letters:
                revealed_word += char + " "
            else:
                revealed_word += "_ "
        print(revealed_word)

    def get_letter(self) -> str:
        while True:
            try:
                letter = input("Please guess the letter: ").lower()
                if letter.isalpha() and len(letter) == 1:
                    return letter
                else:
                    print("Please enter a valid single letter.")
            except KeyboardInterrupt:
                print("\nExiting...")
                exit(0)
            except Exception as error:
                print(f"Error: {error}")

    def get_word(self) -> str:
        while True:
            try:
                guessed_word = input("Please guess the word: ").lower()
                if guessed_word.isalpha():
                    return guessed_word
                else:
                    print("Please enter a valid word.")
            except KeyboardInterrupt:
                print("\nExiting...")
                exit(0)
            except Exception as error:
                print(f"Error: {error}")

    def process_word_guess(self) -> bool:
        guessed_word = self.get_word()
        if guessed_word == self.word:
            print("Congratulations! You've guessed the word correctly.")
            return True
        else:
            print(f"Sorry, wrong word. The word was: '{self.word.upper()}'. GAME OVER.")
            return False

    def check_guess_limit(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if len(args[0]) < 10:
                return func(self, *args, **kwargs)
            else:
                print("You have guessed 10 letters. Please guess the word.")
                self.process_word_guess()
                exit(0)

        return wrapper

    @check_guess_limit
    def process_letter_guess(self, used_letters_list: list) -> bool:
        guessed_letter = self.get_letter()
        if guessed_letter:
            if guessed_letter in used_letters_list:
                print(f"You've already guessed the letter '{guessed_letter}'.")
                return True
            used_letters_list.append(guessed_letter)
            if guessed_letter in self.word:
                print(f"The letter '{guessed_letter}' is in the word.")
                return True
            else:
                print(f"The letter '{guessed_letter}' is not in the word.")
                return False