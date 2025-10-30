from flask import Flask
from flask_login import LoginManager
from web.models import db, User
import os

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "static")
    )

    # Secret key
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')

    # SQLite in /tmp for serverless
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL',
        'sqlite:////tmp/database.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views)
    app.register_blueprint(auth, url_prefix='/auth')

    # Login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Create tables safely
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print("DB creation error:", e)

    return app