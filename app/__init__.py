from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Make this a random string!'
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.static_folder = 'static'

from app import routes