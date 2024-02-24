from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from grocery_app.models import User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from grocery_app.config import Config
from grocery_app.main.routes import main
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

app.register_blueprint(main)

with app.app_context():
  db.create_all()