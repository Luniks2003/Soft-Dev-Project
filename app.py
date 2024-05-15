from flask import Flask, render_template, flash, request, redirect, url_for
from distutils.log import debug 
from fileinput import filename 
from flask import *
import os
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import aspose.ocr as ocr
import easyocr

pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'

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
            print("pytesseract: \n" + extract_text_from_image_pytesseract(UPLOAD_FOLDER+filename))
            print("aspose: \n" + extract_text_from_image_aspose(UPLOAD_FOLDER+filename))
            print("easyocr: \n")
            extract_text_from_image_easyocr(UPLOAD_FOLDER+filename)
            return redirect(request.url)
    return render_template("convert.html")

@app.route("/success/<name>")
def success(name = None):
    return render_template("success.html", name = name)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
def extract_text_from_image_pytesseract(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_image_aspose(image_path):
    # Initialize an instance of Aspose.OCR API
    api = ocr.AsposeOcr()
    # Add image to the recognition batch
    input = ocr.OcrInput(ocr.InputType.SINGLE_IMAGE)
    input.add(image_path)
    # Extract and show text
    results = api.recognize_handwritten_text(input)
    text = results[0].recognition_text
    return text

def extract_text_from_image_easyocr(image_path):
    
    reader = easyocr.Reader(['en']) # specify the language  
    result = reader.readtext(image_path)

    for (bbox, text, prob) in result:
        print(f'Text: {text}, Probability: {prob}')
        
