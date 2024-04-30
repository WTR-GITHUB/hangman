## SCALE DOWN TASK (maximum score : 7-8):

**TASK:**  
Create a Hangman Game (terminal version). [Watch Hangman Game](https://www.youtube.com/watch?v=leW9ZotUVYo)

- Maximum guess attempts: 10.
- Ability to guess a word or a letter. If a guess is incorrect, the user loses 1 life.
- If the user has 0 guesses (lifes) left, the game is lost.

**REQUIREMENTS:**

- Create a new GITHUB project, virtual env, README, .gitignore, etc.
- Use python functions and/or classes to achieve necessary functionality.
- Possible words should be held in a list data structure.
- Use type annotations.
- Use `print` or logging library to log out information.

---

## FULL TASK (maximum score 10):

**TASK:**  
Create a Hangman Game (GUI/terminal version). [Watch Hangman Game](https://www.youtube.com/watch?v=leW9ZotUVYo)

- Maximum guess attempts: 10.
- Ability to guess a word or a letter. If a guess is incorrect, the user loses 1 life.
- If the user has 0 guesses (lifes) left, the game is lost. (Give options to see all-time results or start a new game)

**REQUIREMENTS:**

- Create a new GITHUB project, virtual env, README, .gitignore, etc.
- Use OOP structures (classes, inheritance, dataclasses, modules) to construct game backend logic.
- For the front-end part, you can use CLI, but a Flask application is preferable.
- Create user registration (name, surname, email), store it using an SQL database.
- Use MongoDB to store all necessary game data.
- At least one of the system parts (front-end/back end) should be dockerized.
- Use type annotations, error handling throughout the code.
- Use a logging library to log out information (terminal and files).
- Unit tests to cover most important functionality.
- After the game session, show a table with user information: games played today, games won/lost today, guesses made.

**Nice to have:**

- All system parts should be dockerized.
- Shell script to run the program automatically.
- Show TOP 10 performances of all accounts (create a button to see that table from the game panel).
- Music sounds on good/bad guesses.
