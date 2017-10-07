from flask import Flask, request
import os, webbrowser
from mongo import *
from db import DB_NAME, DB_URI



app = Flask(__name__)

# DB_URI is in the db.py file
app.config['MONGOALCHEMY_DATABASE'] = DB_NAME
app.config['MONGOALCHEMY_CONNECTION_STRING'] = DB_URI

# initialize the database
db.init_app(app)

# upload specs
UPLOAD_FOLDER = 'temp/'
ALLOWED_EXTENSTIONS = set(['png', 'jpg', 'jpeg', 'bmp'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER