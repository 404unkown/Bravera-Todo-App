import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Use environment variables for production (Vercel) or defaults for local
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'sqlite:///tmp/database.db'  # fallback for local development
    )
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Import views and auth after app creation
    from . import views, auth
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(views.main_bp)

    # Initialize the database
    db.init_app(app)

    # Create tables if they don't exist
    with app.app_context():
        db.create_all()

    return app