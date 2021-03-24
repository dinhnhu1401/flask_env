from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '0007e0e77196b310f124fb653e1ef277'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temp.db'

# print(app.config)
db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manger = LoginManager(app)
login_manger.login_view = 'login'
login_manger.login_message_category = 'info'


from flask_env import routes