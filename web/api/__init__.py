import os
import logging
from modules.logger import create_file_handler
from flask import Flask
from web.api import views
from flask_cors import CORS


SECRET_KEY = os.getenv('SECRET_KEY', '_5#y2L"F4Q8zg234ashh30a]/')


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.secret_key = SECRET_KEY
views.init_app(app)
if not app.debug:
    app.logger.addHandler(create_file_handler("api.log"))
else:
    CORS(app, supports_credentials=True)
