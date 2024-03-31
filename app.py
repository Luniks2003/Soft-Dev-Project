from flask import Flask, render_template, flash, request, redirect, url_for
from distutils.log import debug 
from fileinput import filename 
from flask import *
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'html', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about(name = None):
    return render_template("about.html")

@app.route("/convert")
def convert():
    return render_template("convert.html")

@app.route("/success", methods = ['GET', 'POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save(app.config['UPLOAD_FOLDER'] + f.filename)
    return render_template("success.html", name = f.filename)
