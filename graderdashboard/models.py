from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
# Models with Flask-SQLAlchemy
db = SQLAlchemy()

class Grade(db.Model):
    __tablename__ = 'grades'

    name = db.Column(db.String(80))
    question = db.Column(db.String(80))
    score = db.Column(db.Float)
    submission_time = db.Column(db.DateTime, primary_key=True)

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
