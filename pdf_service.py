from flask import Flask, request, jsonify
import fitz
import os

def extract_form_field_positions(pdf_path):
    pages = []
    
    field_positions = []
    
    document = fitz.open(pdf_path)
    
    for page in document:
        pages.append({
            'number': page.number,
            'rect': {
                'offset_left': page.rect.x0,
                'offset_top': page.rect.y0,
                'width': page.rect.width,
                'height': page.rect.height
            }
        })
        for field in page.widgets():
            field_positions.append({
                'field_name': field.field_name,
                'field_label': field.field_label,
                'field_type': field.field_type,
                'rect': {
                    'offset_left': field.rect.x0,
                    'offset_top': field.rect.y0,
                    'width': field.rect.width,
                    'height': field.rect.height
                }
            })
    
    document.close()
    
    return {
        'pages': pages,
        'fields': field_positions
    }

app = Flask(__name__)

@app.route('/')
def index():
    return 'PDF Service'

@app.route('/extract-fields', methods=['POST'])
def extract_fields():
    # Save the uploaded file
    pdf_file = request.files['file']
    pdf_filename = os.path.join('/tmp', pdf_file.filename)
    pdf_file.save(pdf_filename)
    
    # Extract field positions
    fields_data = extract_form_field_positions(pdf_filename)
    
    # Remove the temporary file
    os.remove(pdf_filename)
    
    # Return the field data
    return jsonify(fields_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)