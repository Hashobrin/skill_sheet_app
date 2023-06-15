import os
from pathlib import Path
from datetime import datetime, date, time

import flask
from flask import (
    Flask, request, url_for, render_template,
    redirect, flash, session, send_from_directory,
)
from flask.views import View
from flask_login import (
    LoginManager, UserMixin, login_user,
    login_required, logout_user, current_user
)

from src import app, db
from src.forms import (
    LoginForm, SignupForm, EditProfileForm, EditMySkillForm, ChangePassword)
from src.models import User, Skill


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static/images'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon',
    )


class SayHelloView(View):
    def __init__(self, template) -> None:
        self.template = template

    def dispatch_request(self):
        return render_template('sayhello.html')


app.add_url_rule(
    '/sayhello',
    view_func=SayHelloView.as_view('say_hello', 'sayhello.html')
)


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
def signup_get():
    return render_template('signup.html', form=SignupForm())


@app.route('/signup', methods=['post'])
def signup_post():
    input_email = request.form.get('email')
    input_password = request.form.get('password')
    input_retype = request.form.get('retype')
    user_exists = User.query.filter_by(email=input_email).first()

    if input_password == input_retype:
        if user_exists:
            flash('This E-mail address is already exists.')
            return redirect(url_for('signup'))
        else:
            user = User(
                email=input_email,
                password=input_password,
                first_name=None,
                last_name=None,
                gender=None,
                birthday=None,
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('home'))
    else:
        flash('Disagreed password.')
        return redirect(url_for('signup'))


@app.route('/user/<int:id_>', methods=['get'])
def mypage_get(id_):
    user = User.query.get(id_)
    skill_list = Skill.query.filter_by(user_id=user.id).all()
    return render_template(
        'mypage.html', id_=id_, user_data = user, skill_list=skill_list)


@login_required
@app.route('/edit_my_skill', methods=['post'])
def mypage_post():
    skill = Skill(name=request.form.get('skill_name'), user_id=current_user.id)
    db.session.add(skill)
    db.session.commit()
    return redirect(url_for('edit_profile'))


@login_required
@app.route('/edit_profile', methods=['get'])
def edit_profile_get():
    user = User.query.get(current_user.id)
    edit_profile_form = EditProfileForm(
        request.form,
        first_name=user.first_name,
        last_name=user.last_name,
        gender=user.gender,
        birth_year=user.birthday.year,
        birth_month=user.birthday.month,
        birth_date=user.birthday.day,
    )
    skill_list = Skill.query.filter_by(user_id=user.id).all()
    
    return render_template(
        'edit_profile.html',
        form=edit_profile_form,
        skill_list=skill_list,
    )


@login_required
@app.route('/edit_profile', methods=['post'])
def edit_profile_post():
    user = User.query.get(current_user.id)
    user.first_name = request.form.get('first_name')
    user.last_name = request.form.get('last_name')
    user.gender = request.form.get('gender')
    birth_year = request.form.get('birth_year')
    birth_month = request.form.get('birth_month')
    birth_date = request.form.get('birth_date')
    user.birthday = datetime.strptime(
        f'{birth_year}-{birth_month}-{birth_date}', '%Y-%m-%d')
    
    skill = Skill(name=request.form.get('skill_name'), user_id=current_user.id)
 
    db.session.merge(user)
    db.session.add(skill)
    db.session.commit()
    flash('Updated your profile.')
    return redirect(url_for('mypage'))


@login_required
@app.route('/delete_skill/<int:id>', methods=['get'])
def delete_skill(id):
    skill = Skill.query.get(id)
    db.session.delete(skill)
    db.session.commit()
    return redirect(url_for('edit_profile'))


@login_required
@app.route('/change_password', methods=['get'])
def change_password_page():
    return render_template('change_password.html', form=ChangePassword())


@login_required
@app.route('/change_password', methods=['post'])
def change_password():
    user = User.query.get(current_user.id)
    form = ChangePassword()
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    retype = request.form.get('retype')

    if form.validate_on_submit():
        if old_password == user.password and new_password == retype:
            user.password = request.form.get('new_password')
            db.session.merge(user)
            db.session.commit()
            flash('Changed your password.')
            return redirect(url_for('mypage'))

    flash('Wrong password.')
    return render_template('change_password.html', form=form)

