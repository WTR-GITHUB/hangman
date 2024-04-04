from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'MyHangman'
POSTGRES_DB = 'postgres'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'  

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50), nullable=False)
    progress_percentage = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Progress(task_name='{self.task_name}', progress_percentage={self.progress_percentage})"


@app.route('/create_table')
def create_table():
    try:
        db.create_all()
        return 'Progress table created successfully!', 200
    except Exception as e:
        return f'An error occurred: {e}', 500
    

@app.route('/delete_table')
def delete_table():
    try:
        db.drop_all()
        return 'Progress table deleted successfully!', 200
    except Exception as e:
        return f'An error occurred: {e}', 500

if __name__ == '__main__':
    app.run(debug=True)
