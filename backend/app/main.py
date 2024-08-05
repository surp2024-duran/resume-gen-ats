# backend/app/main.py
import sys
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.routes import main_routes

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = os.getenv("MONGO_FULL_URI")
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=True)
