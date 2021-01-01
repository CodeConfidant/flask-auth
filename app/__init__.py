from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Make this a random string!'
app.static_folder = 'static'

from app import routes