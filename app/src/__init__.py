import os
from pathlib import Path

import flask
from flask import (
    Flask, request, url_for, render_template,
    redirect, flash, session, send_from_directory,
)
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy



base_dir = os.path.dirname(__file__)

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

# app.config['SECRET_KEY'] = 'secretkey'
# db_url = 'sqlite:///' + os.path.join(base_dir, 'db.sqlite')
# app.config['SQLALCHEMY_DATABASE_URI'] = db_url
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_NATIVE_UNICODE'] = 'utf-8'
config_type = {'development': 'config.Development',}
app.config.from_object(
    config_type.get(os.getenv('FLASK_APP_ENV', 'development')))
db = SQLAlchemy(app)
# db.init_app(app)
migrate = Migrate(app, db)

from src import views
from src.models import User

@app.before_first_request
def init():
    db.create_all()
    

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
