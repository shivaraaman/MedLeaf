from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
from keras.models import load_model
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the uploaded file
    file_path = os.path.join(r"D:\COLLEGE\outfit-repo\flask", file.filename)
    file.save(file_path)
    print(file_path)
    return jsonify({'message': 'File uploaded successfully', 'file_path': file_path})

@app.route('/get_input', methods=['POST'])
def get_input():
    data = request.json
    file_path = data.get('file_path')
    print(file_path)
    if not file_path:
        return jsonify({'error': 'File path not provided'})

    class_names = []
    directory_path = r"D:\COLLEGE\SEMESTER-5\PROJECT\Test-CNN\Data\train"
    file_names = os.listdir(directory_path)
    for file_name in file_names:
        class_names.append(file_name)

    model_path = r"D:\COLLEGE\SEMESTER-5\PROJECT\ML.h5"
    model = load_model(model_path)

    img = tf.keras.preprocessing.image.load_img(file_path, target_size=(128, 128))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = np.array([img_array])

    predictions = model.predict(img_array)
    class_id = np.argmax(predictions, axis=1)
    predicted_class = class_names[class_id.item()]
    print(predicted_class)

    return jsonify({'predicted_class': predicted_class})

if __name__ == '__main__':
    app.run(debug=True)
