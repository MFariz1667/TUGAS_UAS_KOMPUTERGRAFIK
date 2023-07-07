#app.py
from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('edit_image.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return {
        'top_left': img[:size, :size],
        'top_center': img[:size, width // 2 - size // 2:width // 2 + size // 2],
        'top_right': img[:size, width - size:width],
        'center_left': img[height // 2 - size // 2:height // 2 + size // 2, :size],
        'center': img[height // 2 - size // 2:height // 2 + size // 2, width // 2 - size // 2:width // 2 + size // 2],
        'center_right': img[height // 2 - size // 2:height // 2 + size // 2, width - size:width],
        'bottom_left': img[height - size:height, :size],
        'bottom_center': img[height - size:height, width // 2 - size // 2:width // 2 + size // 2],
        'bottom_right': img[height - size:height, width - size:width],
    }[position]

def crop_image(img, position, size):
    cropped_img = crop_by_position(img, position, size)
    _, buffer = cv2.imencode('.jpg', cropped_img)
    cropped_bytes = base64.b64encode(buffer)
    return cropped_bytes

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('edit_image.html')

    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['file']
    position = request.form['position']
    size = int(request.form['size'])

    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    if file and allowed_file(file.filename):
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        cropped_bytes = crop_image(img, position, size)
        return cropped_bytes

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}

if __name__ == '__main__':
    app.run()
