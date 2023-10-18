from flask import Flask, render_template, request, send_file
from stegano import lsb
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

def embed_message(input_image_path, text):
    output_image_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'embedded_image.png')
    secret_message = lsb.hide(input_image_path, text)
    secret_message.save(output_image_path)
    return output_image_path

def extract_message(image_path):
    extracted_message = lsb.reveal(image_path)
    return extracted_message

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        uploaded_file = request.files['image']
        text = request.form['text']

        if uploaded_file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(filename)

            embedded_image = embed_message(filename, text)
            return render_template('download.html', message="Data embedded successfully!", image=embedded_image)

    return render_template('home.html')

@app.route('/extract', methods=['POST'])
def extract():
    extracted_message = None

    if request.method == 'POST':
        print(request.form)  # This prints the form data
        uploaded_file = request.files.get('image')

        if uploaded_file:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(image_path)
            extracted_message = extract_message(image_path)

    return render_template('extract.html', extracted_message=extracted_message)

# @app.route('/downloads/embedded_image.png', methods=['GET'])
# def download():
#     image_path = 'embedded_image.png'  # Replace with the path to your image file
#     print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF",image_path)
#     return send_file(image_path, as_attachment=True)

@app.route('/download_embedded_image')
def download_embedded_image():
    embedded_image_path = os.path.join(app.config['DOWNLOAD_FOLDER'], 'embedded_image.png')
    return send_file(embedded_image_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
