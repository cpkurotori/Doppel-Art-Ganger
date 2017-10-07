from flask import Flask, request
import os, webbrowser
from mongo import *
from db import DB_NAME, DB_URI
from flask import render_template
from mongo import *

app = Flask(__name__)

# DB_URI is in the db.py file
app.config['MONGOALCHEMY_DATABASE'] = DB_NAME
app.config['MONGOALCHEMY_CONNECTION_STRING'] = DB_URI

# initialize the database
db.init_app(app)

# upload specs
UPLOAD_FOLDER = 'temp/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'bmp'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# secret key
app.secret_key = 'XqRByek'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS