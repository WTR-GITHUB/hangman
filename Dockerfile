FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . /app

# Expose the port the app runs on
EXPOSE 5011

# Command to run the Flask application
ENTRYPOINT [ "python" ]

CMD ["hangman.py"]
