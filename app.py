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
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
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
        if 'upload' in request.form:
        # check if the post request has the file part
            if 'file' not in request.files:
                return redirect(request.url)
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                converted_text = detect_handwriting(UPLOAD_FOLDER + filename)
                return render_template("convert.html", converted_text = converted_text)
        elif 'download' in request.form:
            # Get text from POST request
            text_data =  request.form.get('text') 
            # Process the text data as needed
            print(f"Received text data: {text_data}")
            return send_file(create_file(text_data), as_attachment=True)
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

def create_file(edited_text):
    filename = generate_random_filename(24,'txt')
    file = open('extracted-text-files/' + filename, 'w')
    file.write(edited_text)
    file.close
    text_file_name = 'extracted-text-files/' + filename
    
    return text_file_name

import random
import string


def generate_random_filename(length: int = 24, extension: str = "") -> str:
    """Generates a random filename"""
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(length))
    if extension:
        if "." in extension:
            pieces = extension.split(".")
            last_extension = pieces[-1]
            extension = last_extension
        return f"{random_string}.{extension}"
    return random_string

if __name__ == '__main__':
    app.run(debug=True)