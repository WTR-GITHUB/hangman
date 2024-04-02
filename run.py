import random

class Word:
    def __init__(self):
        self.word = self.random_word()

    def random_word(self):
        with open("words.txt", "r") as data:
            words_list = data.read().splitlines()
        word = random.choice(words_list)
        print(word)
        print(len(word))
        return word

    def display_word(self, letters: list):
        revealed_word = ""
        for char in self.word:
            if char in letters:
                revealed_word += char + " "
            else:
                revealed_word += "_ "
        print(revealed_word)

if __name__ == "__main__":
    word_game = Word()

    letters = ["a", "e", "i", "o", "u"]

    word_game.display_word(letters)
