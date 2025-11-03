from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    progress = db.relationship('UserProgress', backref='user', lazy=True)
    test_results = db.relationship('TestResult', backref='user', lazy=True)
    word_progress = db.relationship('WordProgress', backref='user', lazy=True)
    verb_progress = db.relationship('VerbProgress', backref='user', lazy=True)
    activity_logs = db.relationship('ActivityLog', backref='user', lazy=True)

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    german = db.Column(db.String(100), nullable=False)
    english = db.Column(db.String(100), nullable=False)
    article = db.Column(db.String(10))  # der, die, das
    level = db.Column(db.String(10), default='A1')  # A1, A2, B1, B2, C1

class Verb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    infinitive = db.Column(db.String(100), nullable=False)
    english = db.Column(db.String(100), nullable=False)
    ich = db.Column(db.String(100), nullable=False)
    du = db.Column(db.String(100), nullable=False)
    er_sie_es = db.Column(db.String(100), nullable=False)
    wir = db.Column(db.String(100), nullable=False)
    ihr = db.Column(db.String(100), nullable=False)
    sie_Sie = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(10), default='A1')  # A1, A2, B1, B2, C1

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_time_minutes = db.Column(db.Integer, default=0)
    words_learned = db.Column(db.Integer, default=0)
    verbs_learned = db.Column(db.Integer, default=0)

class WordProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    times_seen = db.Column(db.Integer, default=0)
    times_correct = db.Column(db.Integer, default=0)
    times_incorrect = db.Column(db.Integer, default=0)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    priority_score = db.Column(db.Float, default=100.0)  # Higher = more likely to be shown

class VerbProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    verb_id = db.Column(db.Integer, db.ForeignKey('verb.id'), nullable=False)
    times_seen = db.Column(db.Integer, default=0)
    times_correct = db.Column(db.Integer, default=0)
    times_incorrect = db.Column(db.Integer, default=0)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    priority_score = db.Column(db.Float, default=100.0)  # Higher = more likely to be shown

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    test_type = db.Column(db.String(20), nullable=False)  # 'vocabulary' or 'verb'
    is_mock = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    # For tracking individual answers
    answers = db.relationship('TestAnswer', backref='test', lazy=True)

class TestAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test_result.id'), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=True)
    verb_id = db.Column(db.Integer, db.ForeignKey('verb.id'), nullable=True)
    user_answer = db.Column(db.String(200))
    correct_answer = db.Column(db.String(200))
    is_correct = db.Column(db.Boolean)

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer, default=0)
