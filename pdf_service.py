from flask import Flask, request, jsonify
from fitz import *  # PyMuPDF
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return 'PDF Service'

@app.route('/extract-fields', methods=['POST'])
def extract_fields():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        file_path = temp_file.name
        file.save(temp_file)

    try:
        with fitz.open(file_path) as document:
            pages = [
                {
                    'number': page.number,
                    'w': page.rect.width,
                    'h': page.rect.height,
                    'fields': [
                        {
                            'name': field.field_name,
                            'label': field.field_label,
                            'type': field.field_type,
                            'on_state': field.on_state(),
                            'x': field.rect.x0,
                            'y': field.rect.y0,
                            'w': field.rect.width,
                            'h': field.rect.height
                        }
                        for field in page.widgets()
                    ]
                }
                for page in document
            ]
    finally:
        os.remove(file_path)
    
    return jsonify(pages)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
