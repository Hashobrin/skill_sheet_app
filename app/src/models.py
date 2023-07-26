from datetime import datetime, date, time

from flask_login import (
    UserMixin, login_user, login_required, logout_user, current_user)
from sqlalchemy import (
    Column, Integer, String, DateTime, Date, Time, desc
)

from src import db


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(Integer, primary_key=True)
    email = db.Column(String(255), unique=True, nullable=False)
    password = db.Column(String(255), nullable=False)
    first_name = db.Column(String(255))
    last_name = db.Column(String(255))
    gender = db.Column(String(255))
    birthday = db.Column(Date, default=date.today())
    # skills = db.relationship('Skill', backref='users', lazy=True)


    def __init__(
        self, email, password, first_name, last_name, gender, birthday
    ):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birthday = birthday


class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(Integer, primary_key=True, nullable=False)
    name = db.Column(String(255), nullable=False)
    user_id = db.Column(Integer, db.ForeignKey('users.id'))
    start_date = db.Column(Date, default=date.today())


    def __init__(self, name, user_id, start_date):
        self.name = name
        self.user_id = user_id
        self.start_date = start_date
        