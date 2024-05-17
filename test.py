import io
import os
from google.cloud import vision

# Set up authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'htr-project-school-2139d4c4aec4.json'

# Initialize the Vision API client
client = vision.ImageAnnotatorClient()

def detect_handwriting(path):
    # Detects handwritten text in the file.
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    
    # Extracting text
    annotations = response.text_annotations
    if annotations:
        print('Detected handwriting:')
        for annotation in annotations:
            print(annotation.description)
    else:
        print('No handwriting detected.')
    
    if response.error.message:
        raise Exception(f'{response.error.message}')

# Test with an image file
image_path = 'uploads/438270987_1544531489456974_6711786784439356146_n.jpg'
detect_handwriting(image_path)
