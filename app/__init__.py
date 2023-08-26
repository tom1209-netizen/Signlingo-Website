from flask_bcrypt import Bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


app = Flask(__name__, static_folder="static")
app.config.from_object('app.config.app_config')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

from app import routes
