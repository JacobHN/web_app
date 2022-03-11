from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from webapp.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

bcrypt = Bcrypt()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from webapp.main.routes import main
    from webapp.account.routes import account
    from webapp.post.routes import post

    app.register_blueprint(main)
    app.register_blueprint(account)
    app.register_blueprint(post)

    return app