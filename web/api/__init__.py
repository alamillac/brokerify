import logging
from modules.logger import create_file_handler
from flask import Flask
from web.api import views


logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
views.init_app(app)
if not app.debug:
    app.logger.addHandler(create_file_handler("api.log"))
