from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow import keras
import io
import base64

app = Flask(__name__)
CORS(app)

# Modell beim Start laden
print("Lade MNIST Modell...")
try:
    model = keras.models.load_model('mnist_model.keras')
    print("✓ Modell erfolgreich geladen!")
except Exception as e:
    print(f"✗ Fehler beim Laden des Modells: {e}")
    model = None

@app.route('/')
def home():
    return jsonify({
        'status': 'Backend läuft',
        'model_loaded': model is not None,
        'endpoints': [
            '/predict - POST: Sendet Bild für Vorhersage',
            '/health - GET: Überprüft Backend-Status'
        ]
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Modell nicht geladen'}), 500

    try:
        # Empfange Bild
        if 'image' not in request.files:
            # Alternative: Base64-kodiertes Bild
            data = request.get_json()
            if data and 'image' in data:
                # Base64-Bild dekodieren
                image_data = data['image']
                if ',' in image_data:
                    image_data = image_data.split(',')[1]
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))
            else:
                return jsonify({'error': 'Kein Bild gefunden'}), 400
        else:
            # Normaler File-Upload
            file = request.files['image']
            image = Image.open(file.stream)

        # Bild vorverarbeiten
        # In Graustufen konvertieren
        image = image.convert('L')

        # Auf 28x28 skalieren
        image = image.resize((28, 28))

        # In NumPy-Array umwandeln
        img_array = np.array(image)

        # Normalisieren (0-255 -> 0-1)
        img_array = img_array.astype('float32') / 255.0

        # Reshape für das Modell (1, 28, 28)
        img_array = np.expand_dims(img_array, axis=0)

        # Vorhersage machen
        predictions = model.predict(img_array, verbose=0)
        predicted_digit = int(np.argmax(predictions[0]))
        confidence = float(predictions[0][predicted_digit])

        # Alle Wahrscheinlichkeiten zurückgeben
        all_probabilities = {
            str(i): float(predictions[0][i])
            for i in range(10)
        }

        return jsonify({
            'prediction': predicted_digit,
            'confidence': confidence,
            'all_probabilities': all_probabilities
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/reload', methods=['POST'])
def reload_model():
    global model
    try:
        model = keras.models.load_model('mnist_model.keras')
        return jsonify({'status': 'reloaded', 'model_loaded': model is not None})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("🚀 Flask Backend wird gestartet...")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)
