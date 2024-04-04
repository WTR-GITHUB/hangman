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


word_game = Word()
used_letters_list = []
error_count = 0

word_game.display_word(used_letters=used_letters_list)

word_game.word

while True:
    print("Please choose:")
    print("1. Guess a letter")
    print("2. Guess the word")
    user_choice = input()

    if user_choice == "1":
        if not word_game.process_letter_guess(used_letters_list):
            error_count += 1
            if error_count == 6:
                print(
                    f"You've reached the maximum number of errors. The word was: '{word_game.word.upper()}'. GAME OVER."
                )
                exit(0)
        word_game.display_word(used_letters_list)
        print(f"Already used letters: {used_letters_list}")
        print(f"Wrong guessed letters {error_count} of 6")

    elif user_choice == "2":
        if word_game.process_word_guess():
            break

    else:
        print("Please input correct choice!")

    if set(word_game.word) == set(used_letters_list):
        print("Congratulations! You've guessed the word correctly.")
        break


