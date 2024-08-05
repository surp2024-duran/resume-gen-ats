# backend/app/__init__.py
from flask import Flask
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.routes import main_routes

def create_app():
    app = Flask(__name__)

    app.register_blueprint(main_routes)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
