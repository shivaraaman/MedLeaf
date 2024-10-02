import os
from flask import Flask, render_template, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import uuid
import pandas as pd
app = Flask(__name__)

UPLOAD_FOLDER = r'D:\COLLEGE\SEMESTER-5\PROJECT\Final_proj\image_input'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def infoextract(indexnum):
    df=pd.read_csv(r'C:\Users\shiva\Downloads\plant_classification.csv')
    a=df['Botanical Name'][indexnum]
    l=[df['Botanical Name'][indexnum],df['Common Name'][indexnum],df['Family'][indexnum],df['Bioactive Compounds'][indexnum],df['Traditional Uses'][indexnum]]
    return l
    


def preprocess_image(image):
    image = image.resize((128, 128))
    image_array = np.array(image)
    image_array = image_array / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

def classify(image_path):
    try:
        print("Image path:", image_path)  # Print image path for debugging
        if not os.path.isfile(image_path):
            raise FileNotFoundError("Image file not found")
        
        model = load_model(r"D:\COLLEGE\SEMESTER-5\PROJECT\trained data\final_data.h5")
        image = Image.open(image_path)
        preprocessed_image = preprocess_image(image)
        predictions = model.predict(preprocessed_image)
        predicted_class_index = np.argmax(predictions)
        predicted_class = int(predicted_class_index)
        infoofindex=infoextract(predicted_class)
        return {'info':infoofindex}
    except Exception as e:
        return {'error': str(e)}


@app.route('/')
def index():
    return render_template('templates\index.html')

@app.route('/process-image', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        image_data = request.files['image']
        if image_data.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        filename = str(uuid.uuid4()) + '.png'
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_data.save(image_path)

        # Classify the image
        result = classify(image_path)
        print(result)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':    app.run(debug=True)
