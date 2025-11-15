from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
from tensorflow import keras
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

model = keras.models.load_model("mnist_model.keras")
print("MNIST Model Loaded")
print("="*60)

@app.route('/')
def home():
    return jsonify({'Status': 'Welcome to my app!', "endpoint": "/api/predict"})

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        # Get file from request - Frontend sends 'file'
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'Keine Datei hochgeladen'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'success': False, 'error': 'Keine Datei ausgewählt'}), 400

        # Read and process image
        img = Image.open(io.BytesIO(file.read())).convert('L')  # Convert to grayscale
        img = img.resize((28, 28))  # Resize to 28x28
        img_array = np.array(img).astype('float32') / 255.0  # Normalize

        # WICHTIG: Bild invertieren (weißer Hintergrund -> schwarzer Hintergrund)
        # MNIST hat schwarzen Hintergrund mit weißen Ziffern
        if np.mean(img_array) > 0.5:  # Wenn heller Hintergrund
            img_array = 1.0 - img_array  # Invertieren

        img_array = img_array.reshape(1, 28, 28)  # Reshape for model input

        # Make prediction
        predictions = model.predict(img_array, verbose=0)
        predicted_class = np.argmax(predictions, axis=1)[0]
        confidence = float(np.max(predictions))

        # Get all probabilities for visualization
        all_probabilities = predictions[0].tolist()
        probabilities_dict = {str(i): round(float(prob) * 100, 2) for i, prob in enumerate(all_probabilities)}

        # Return response in format expected by frontend
        return jsonify({
            'success': True,
            'prediction': int(predicted_class),
            'confidence': round(confidence * 100, 2),
            'probabilities': probabilities_dict
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
