from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Set the maximum content length for uploads (500 MB in this case)
app.config['MAX_CONTENT_LENGTH'] = 2000 * 1024 * 1024  # 2000 MB
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    return jsonify({"message": f"File uploaded successfully: {file.filename}"}), 200

if __name__ == '__main__':
    app.run(debug=True)
