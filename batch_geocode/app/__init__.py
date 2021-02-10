from flask import Flask
from batch_geocode.config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
app.static_folder = 'static'

from batch_geocode.app import routes