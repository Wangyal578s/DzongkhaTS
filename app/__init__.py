# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)

    # Optional: place for configuration (secret key, DB, uploads)
    app.config['SECRET_KEY'] = 'dev-key-change-later'

    # Import and register routes
    from .routes import bp
    app.register_blueprint(bp)

    return app
