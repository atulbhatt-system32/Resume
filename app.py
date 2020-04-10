from flask import Flask
from flask import render_template, request
import os

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("index.html")

@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template("Home.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        print("hello")
        
    return render_template("resume.html")