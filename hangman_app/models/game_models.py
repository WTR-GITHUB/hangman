from hangman_app import mongodb

class Word:
    def __init__(self):
        self.word = self.random_word()

    def random_word(self) -> str:
        random_word_document = mongodb.collection.aggregate([{"$sample": {"size": 1}}])
        random_word = random_word_document.next()["word"]
        return random_word

    def display_word(self, used_letters: list) -> str:
        revealed_word = ""
        for char in self.word:
            if char.lower() in used_letters:
                revealed_word += char + " "
            else:
                revealed_word += "_ "
        return revealed_word.strip()

    def process_letter_guess(self, letter: str, used_letters_list: list) -> bool:
        guessed_letter = letter.lower()
        if guessed_letter:
            if guessed_letter in used_letters_list:                
                return True
            used_letters_list.append(guessed_letter)
            if guessed_letter in self.word.lower():                
                return True
            else:                
                return False
            
    def check_all_guessed_letters(self, revealed_letters: list[str]) -> bool:
        unique_word_letters = set(self.word.lower())
        for letter in unique_word_letters:
            if letter not in revealed_letters:
                return False
        return True