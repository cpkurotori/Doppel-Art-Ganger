from flask import Flask
import os, webbrowser

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

PORT = os.getenv('PORT', 8080)
IP = os.getenv('IP', '0.0.0.0')

app.debug = True

app.run(host=IP, port=int(PORT))