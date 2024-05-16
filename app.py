from flask import Flask, render_template, flash, request, redirect, url_for
from distutils.log import debug 
from fileinput import filename 
from flask import *
import os
from werkzeug.utils import secure_filename
from PIL import Image
import io
import os
from google.cloud import vision

app = Flask(__name__)
UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'PNG', 'JPG', 'JPEG', 'PDF'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
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
            print(detect_handwriting(UPLOAD_FOLDER + filename))
            return redirect(request.url)
    return render_template("convert.html")

@app.route("/success/<name>")
def success(name = None):
    return render_template("success.html", name = name)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Set up authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'htr-project-school-2139d4c4aec4.json'

# Initialize the Vision API client
client = vision.ImageAnnotatorClient()

def detect_handwriting(path):
    """Detects handwritten text in the file."""
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    
    # Extracting text
    annotations = response.text_annotations
    if annotations:
        extracted_text = response.text_annotations[0].description
    else:
        extracted_text = 'No handwriting detected.'
    
    if response.error.message:
        raise Exception(f'{response.error.message}')
    
    return extracted_text
