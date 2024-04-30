# Python Beginner Course Final Project

This is my final project for the Python beginner course. The task description is provided in [Task_description.md](https://github.com/WTR-GITHUB/hangman/blob/main/Task_description.md).

The code was developed and tested in a Linux Ubuntu environment. Below are the recommended installation steps.

1. Navigate to the folder where you want to download hangman game folder with the content:
    ```
    cd <folder_name>
    ```

2. Clone this GitHub repository:
    ```
    git clone git@github.com:WTR-GITHUB/hangman.git
    ```
    
3. Navigate to the hangman folder:
    ```
    cd hangman
    ```  

4. Set up a virtual environment:
    ```
    python3 -m venv <venv folder name>
    ```

5. Activate the virtual environment in Linux:
    ```
    source <venv folder name>/bin/activate
    ```

6. Clone this GitHub repository:
    ```
    git clone git@github.com:WTR-GITHUB/hangman.git
    ```

7. Install all necessary requirements:
    ```
    pip install -r requirements.txt
    ```

8. Make necessary configurations in the `docker-compose.yml` file. Essential settings:
    ```yaml
    MAIL_USERNAME: ${MAIL_USERNAME}
    MAIL_PASSWORD: ${MAIL_PASSWORD}
    ```
    All other settings can remain default or be modified according to user needs.

9. Run Docker Compose with the command:
    ```
    docker-compose up --build --force-recreate --no-deps
    ```

10. To stop, use Ctrl+C and the command:
    ```
    docker-compose down
    ```
