import os
from pathlib import Path
from datetime import datetime, date, time

import flask
from flask import (
    Flask, request, url_for, render_template, redirect, flash, session
)
from flask.views import View
from flask_login import (
    LoginManager, UserMixin, login_user,
    login_required, logout_user, current_user
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Column, Integer, String, DateTime, Date, Time, desc
)
import flask_wtf
from wtforms import (
    IntegerField, StringField, PasswordField,
    SubmitField, RadioField, SelectField
)


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(Integer, primary_key=True, nullable=False)
    name = db.Column(String(255), nullable=False)
    user_id = db.Column(Integer, db.ForeignKey('users.id'))


db.create_all()


class LoginForm(flask_wtf.FlaskForm):
    email = StringField('email')
    password = PasswordField('password')
    submit = SubmitField('submit')


class SignupForm(flask_wtf.FlaskForm):
    email = StringField('email')
    password = PasswordField('password')
    retype = StringField('retype')
    submit = SubmitField('submit')


class EditProfileForm(flask_wtf.FlaskForm):
    first_name = StringField('First name')
    last_name = StringField('Last name')
    gender = RadioField(
        label='Gender',
        choices=[('other', 'other'), ('male', 'male'), ('female', 'female')],
    )
    birth_year = SelectField(
        label='Birth year',
        choices=[(x, str(x)) for x in range(1900, datetime.now().year + 1)],
    )
    birth_month = SelectField(
        label='Birth month',
        choices=[(str(y), str(y)) for y in range(1, 13)]
    )
    birth_date = SelectField(
        label='Birth date',
        choices=[(z, str(z)) for z in range(1, 32)],
        # default=5,
    )
    skill_name = SelectField(
        label='Skill name',
        choices=[],
    )
    submit = SubmitField('submit')


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class SayHelloView(View):
    def __init__(self, template) -> None:
        self.template = template

    def dispatch_request(self):
        return render_template('sayhello.html')


app.add_url_rule(
    '/sayhello', view_func=SayHelloView.as_view('say_hello', 'sayhello.html'))


@app.errorhandler(404)
def error_404(error):
    return render_template('404.html')


@app.route('/admin', methods=['get'])
def admin_get():
    users = User.query.all()
    return render_template('admin.html', users=users)


@app.route('/admin/detele/<int:id>', methods=['post'])
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/')
def home():
    users = User.query.all()
    return render_template('home.html', users=users)


@app.route('/login', methods=['get'])
def login_page():
    return render_template('login.html', form=LoginForm())


@app.route('/login', methods=['post'])
def login():
    input_email = request.form.get('email')
    input_password = request.form.get('password')
    user = User.query.filter_by(
        email=input_email, password=input_password).first()

    if user:
        login_user(user)
        return redirect(url_for('home'))
    else:
        flash('Wrong Email or password.')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/signup', methods=['get'])
def signup_page():
    return render_template('signup.html', form=SignupForm())


@app.route('/signup', methods=['post'])
def signup():
    input_email = request.form.get('email')
    input_password = request.form.get('password')
    input_retype = request.form.get('retype')
    user_exists = User.query.filter_by(email=input_email).first()

    if input_password == input_retype:
        if user_exists:
            flash('This E-mail address is already exists.')
            return redirect(url_for('signup'))
        else:
            user = User(email=input_email, password=input_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home'))
    else:
        flash('Disagreed password.')
        return redirect(url_for('signup'))


@login_required
@app.route('/mypage', methods=['get'])
def mypage():
    return render_template('mypage.html')


@login_required
@app.route('/edit_profile', methods=['get'])
def edit_profile_page():
    user = User.query.get(current_user.id)
    form = EditProfileForm(
        request.form,
        first_name=user.first_name,
        last_name=user.last_name,
        gender=user.gender,
        birth_year=user.birthday.year,
        birth_month=user.birthday.month,
        birth_date=user.birthday.day,
        skill_name=Skill.query.filter_by(user_id=user.id)
    )
    return render_template('edit_profile.html', form=form)


@login_required
@app.route('/edit_profile', methods=['post'])
def edit_profile():
    user = User.query.get(current_user.id)
    user.first_name = request.form.get('first_name')
    user.last_name = request.form.get('last_name')
    user.gender = request.form.get('gender')
    birth_year = request.form.get('birth_year')
    birth_month = request.form.get('birth_month')
    birth_date = request.form.get('birth_date')
    user.birthday = datetime.strptime(
        f'{birth_year}-{birth_month}-{birth_date}', '%Y-%m-%d')
    db.session.merge(user)
    db.session.commit()
    flash('Updated your profile.')
    return redirect(url_for('mypage'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
