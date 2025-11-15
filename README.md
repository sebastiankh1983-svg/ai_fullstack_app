# MNIST Backend API

## Projektstruktur

- `NN_Model.py` - Trainiert das MNIST-Modell
- `app.py` - Flask REST API für Vorhersagen
- `mnist_model.keras` - Trainiertes Modell
- `mnist.py` - MNIST Datenverarbeitung

## Installation

### 1. Backend einrichten

```bash
# Virtuelle Umgebung erstellen
python -m venv .venv

# Aktivieren
.venv\Scripts\activate

# Dependencies installieren
pip install tensorflow~=2.20.0 numpy~=2.3.4 flask==3.0.0 flask-cors==4.0.0 pillow>=10.4.0 matplotlib
```

### 2. Modell trainieren (falls noch nicht vorhanden)

```bash
python NN_Model.py
```

Dies erstellt `mnist_model.keras`

### 3. Backend starten

**Option 1 - Batch-Datei:**
```bash
start_backend.bat
```

**Option 2 - Manuell:**
```bash
.venv\Scripts\activate
python app.py
```

Backend läuft auf: http://localhost:5000

## API Endpunkte

### GET /
Status-Information über das Backend

### GET /health
Health-Check Endpunkt

### POST /predict
Sendet ein Bild und erhält eine Vorhersage

**Request:**
- Content-Type: multipart/form-data oder application/json
- Body: 
  - File upload: `image` (PNG/JPG)
  - JSON: `{"image": "base64-encoded-image"}`

**Response:**
```json
{
  "prediction": 7,
  "confidence": 0.99,
  "all_probabilities": {
    "0": 0.01,
    "1": 0.02,
    ...
    "7": 0.99,
    ...
  }
}
```

## Modell-Architektur

**5 Schichten + Input Shape:**
1. Flatten (input_shape=(28, 28)) - Input-Schicht
2. Dense(256) + ReLU - **Dense 1**
3. Dropout(0.3) - **Dropout 1**
4. Dense(128) + ReLU - **Dense 2**
5. Dropout(0.3) - **Dropout 2**
6. Dense(64) + ReLU
7. Dropout(0.2) - **Dropout 3**
8. Dense(10) + Softmax - Output

**Training:**
- Optimizer: Adam (lr=0.001)
- Loss: sparse_categorical_crossentropy
- Epochs: 20
- Batch size: 128

## Fehlerbehebung

### Git Push Fehler (große Dateien)
Die .venv Dateien sind zu groß für GitHub. Lösung:
- `.gitignore` ist bereits konfiguriert
- Nur Source-Code wird committed, nicht .venv/

### Pillow Installation
Falls Pillow 10.1.0 nicht verfügbar:
```bash
pip install pillow>=10.4.0
```

## Technologie-Stack

**Backend:**
- Python 3.13
- TensorFlow 2.20.0
- Flask 3.0.0
- NumPy 2.3.4
- Pillow 10.4.0+

**Model:**
- MNIST Handschrift-Erkennung
- 5 Schichten (Input + Dense + Dropout)
- 99%+ Genauigkeit

