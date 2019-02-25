from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from chatbot.response import ChatBotResponse


app = Flask(__name__)
app.config['SECRET_KEY'] = 'You cannot guess my secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from service_api import models
db.create_all()

CORS(app, resources={r"/api/*": {"origins": "*"}})
chatbot = ChatBotResponse()