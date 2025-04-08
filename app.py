import os
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Folder to save uploaded/converted files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    if file and file.filename.lower().endswith('.jpeg'):
        filename = secure_filename(file.filename)
        jpeg_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Save the uploaded .jpeg file
        file.save(jpeg_path)

        # Rename to .jpg
        jpg_filename = filename.rsplit('.', 1)[0] + '.jpg'
        jpg_path = os.path.join(app.config['UPLOAD_FOLDER'], jpg_filename)
        os.rename(jpeg_path, jpg_path)

        return send_file(jpg_path, as_attachment=True)

    return "Please upload a valid .jpeg file.", 400

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
