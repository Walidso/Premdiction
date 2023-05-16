from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128))
    score = db.Column(db.Integer, default=0)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team1 = db.Column(db.String(64))
    team2 = db.Column(db.String(64))
    result = db.Column(db.String(1))

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'))
    result = db.Column(db.String(1))
