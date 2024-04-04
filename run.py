from models import Word

if __name__ == "__main__":
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
