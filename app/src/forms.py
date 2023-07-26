import os
from pathlib import Path
from datetime import datetime, date, time

from flask_wtf import FlaskForm
from wtforms import (
    IntegerField, StringField, PasswordField,
    SubmitField, RadioField, SelectField, ValidationError,
)


class LoginForm(FlaskForm):
    email = StringField('email')
    password = PasswordField('password')
    submit = SubmitField('Submit')


class SignupForm(FlaskForm):
    email = StringField('email')
    password = PasswordField('password')
    retype = PasswordField('retype')
    submit = SubmitField('Submit')


class EditProfileForm(FlaskForm):
    first_name = StringField('First name')
    last_name = StringField('Last name')
    gender = RadioField(
        label='Gender',
        choices=[('other', 'other'), ('male', 'male'), ('female', 'female')],
    )
    birth_year = SelectField(
        label='Birth year',
        choices = [
            (birth_year_value, str(birth_year_value)) \
            for birth_year_value in range(1900, datetime.now().year+1)
        ],
    )
    birth_month = SelectField(
        label='Birth month',
        choices = [
            (birth_month_value, str(birth_month_value)) \
            for birth_month_value in range(1, 13)],
    )
    birth_date = SelectField(
        label='Birth date',
        choices = [
            (birth_date_value, str(birth_date_value)) \
            for birth_date_value in range(1, 32)],
    )
    skill_name = StringField('skill_name')
    start_year = SelectField(
        label='Start year',
        choices = [
            (start_year_value, str(start_year_value)) \
            for start_year_value in range(1900, datetime.now().year+1)
        ],
    )
    start_month = SelectField(
        label='Start month',
        choices = [
            (start_month_value, str(start_month_value)) \
            for start_month_value in range(1, 13)
        ],
    )
    submit = SubmitField('Submit')


class EditMySkillForm(FlaskForm):
    skill_name = StringField('Skill name')
    submit = SubmitField('Submit')


class ChangePassword(FlaskForm):
    old_password = PasswordField('Password now you setting')
    new_password = PasswordField('New password')
    retype = PasswordField('Retype your new password')
    submit = SubmitField('Submit')

    def validate_new_password(self, new_password):
        if new_password.data == '':
            raise ValidationError('No input.')
        
        if len(new_password.data) < 8:
            raise ValidationError('Password must be 8 charactors or more.')
        
        if new_password.data in ('/', '*', '\\'):
            raise ValidationError('"/", "*" and "\\" are prohibited charactors.')
