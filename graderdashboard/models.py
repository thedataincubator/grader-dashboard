from flask_sqlalchemy import SQLAlchemy
# Models with Flask-SQLAlchemy
db = SQLAlchemy()

class Grade(db.Model):
    __tablename__ = 'grades'

    name = db.Column(db.String(80))
    question = db.Column(db.String(80))
    score = db.Column(db.Float)
    submission_time = db.Column(db.DateTime, primary_key=True)
