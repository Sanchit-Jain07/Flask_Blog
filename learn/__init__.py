from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from learn.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
	
	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)

	from learn.users.routes import users
	from learn.posts.routes import posts
	from learn.main.routes import main

	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)

	return app