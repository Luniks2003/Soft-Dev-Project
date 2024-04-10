from flask import Flask, render_template, flash, request, redirect, url_for
from distutils.log import debug 
from fileinput import filename 
from flask import *
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'PNG', 'JPG', 'JPEG', 'PDF'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about(name = None):
    return render_template("about.html")

@app.route("/convert", methods = ['GET', 'POST'])
def convert():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('success', name=filename))
    return render_template("convert.html")

# @app.route("/success", methods = ['GET', 'POST'])
# def success():
#     # if request.method == 'POST':
#     #     file = request.files['file']
#     #     file.save(app.config['UPLOAD_FOLDER'] + file.filename)
#     return render_template("success.html", name = file.filename)
@app.route("/success/<name>")
def success(name = None):
    return render_template("success.html", name = name)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS