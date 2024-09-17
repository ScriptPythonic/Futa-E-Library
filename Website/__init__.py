from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
import os
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from flask_admin import Admin
import firebase_admin
from firebase_admin import credentials, storage

db = SQLAlchemy()
DB_NAME = "database.db"
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configuration settings
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize Firebase
    cred = credentials.Certificate('./secret.json')  # Path to your Firebase credentials file
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'library-management-92e81.appspot.com'  # Replace with your Firebase app bucket URL
    })

    # Initialize the database
    db.init_app(app)
    migrate.init_app(app, db)

    # Import blueprints
    from .views import views
    from .auth import auth  
    from .borrow import borrow
    from .upload import upload

    # Register blueprints
    app.register_blueprint(borrow, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(upload, url_prefix='/')

    # Initialize Flask-Admin
    admin = Admin(app)

    # Create the database
    from .models import User 
    create_database(app)

    # Set up Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User  
        return User.query.get(int(user_id))

    return app

def create_database(app):
    with app.app_context():
        if not path.exists('Website/' + DB_NAME):
            db.create_all()
