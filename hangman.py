import logging
from logging.handlers import RotatingFileHandler
from hangman_app import app
from hangman_app.utilities.setup_utility import (
    create_database_tables,
    import_words_to_db,
)

# Set up the logging format
formatter = logging.Formatter(
    "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
)

# Set up a rotating log handler to avoid the log file growing indefinitely
log_handler = RotatingFileHandler("app.log", maxBytes=10000, backupCount=1)

# Set the log handler level to DEBUG (or any other level you wish)
log_handler.setLevel(logging.DEBUG)

# Apply the formatter to the log handler
log_handler.setFormatter(formatter)

# Add the log handler to the Flask app's logger
app.logger.addHandler(log_handler)

# Optionally, set the overall log level for the app's logger
app.logger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    with app.app_context():
        create_database_tables()
        import_words_to_db()

    app.run(host="0.0.0.0", port=5011, debug=False)
