# 🚀 Quick Start Guide - MNIST Backend

## Backend starten

### Option 1 - Batch-Datei (empfohlen)
```
start_backend.bat
```

### Option 2 - Manuell
```bash
.venv\Scripts\activate
python app.py
```

✅ Backend läuft auf http://localhost:5000


## Modell trainieren (optional)

Falls du das Modell neu trainieren möchtest:

```bash
.venv\Scripts\activate
python NN_Model.py
```

Dies erstellt/überschreibt `mnist_model.keras`


## API testen

### Health Check
```bash
curl http://localhost:5000/health
```

### Vorhersage (mit Bild)
```bash
curl -X POST -F "image=@pfad/zu/bild.png" http://localhost:5000/predict
```


## Projekt-Struktur

```
Backend/
├── app.py                # Flask REST API
├── NN_Model.py           # Model Training
├── mnist.py              # MNIST Datenverarbeitung
├── mnist_model.keras     # Trainiertes Modell
├── requirements.txt      # Python Dependencies
└── start_backend.bat     # Backend starten
```

### Backend (Python)
- 🐍 Python 3.13
- 🧠 TensorFlow 2.20
- 🌐 Flask 3.0 (REST API)
- 🔄 Flask-CORS (Cross-Origin)
- 🖼️ Pillow (Bildverarbeitung)

### Frontend (JavaScript)
- 📝 Vanilla JavaScript (keine Frameworks!)
- 🎨 CSS3 (Grid, Flexbox, Animations)
- 🖼️ HTML5 Canvas API
- 🚀 Python HTTP Server


## Modell-Informationen

### Architektur
- **Input**: 28x28 Graustufenbild
- **Schichten**: 5 Haupt-Layers
  - Flatten (Input)
  - Dense(256) + Dropout(0.3)
  - Dense(128) + Dropout(0.3)
  - Dense(64) + Dropout(0.2)
  - Dense(10) - Softmax Output

### Training
- **Dataset**: MNIST (60.000 Training, 10.000 Test)
- **Genauigkeit**: ~98.5%
- **Optimizer**: Adam (lr=0.001)
- **Epochs**: 20
- **Batch Size**: 128


## API Endpunkte

### GET `/`
Status-Info über das Backend
```json
{
  "status": "Backend läuft",
  "model_loaded": true
}
```

### GET `/health`
Health Check
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### POST `/predict`
Vorhersage für gezeichnete Ziffer

**Request:**
```json
{
  "image": "data:image/png;base64,iVBORw0KG..."
}
```

**Response:**
```json
{
  "prediction": 7,
  "confidence": 0.99,
  "all_probabilities": {
    "0": 0.001,
    "1": 0.002,
    ...
    "7": 0.990,
    ...
  }
}
```


## Troubleshooting

### Backend startet nicht?
```bash
# Prüfe ob .venv existiert
dir .venv

# Falls nicht, erstelle:
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### "ModuleNotFoundError: No module named 'tensorflow'"?
```bash
.venv\Scripts\activate
pip install tensorflow~=2.20.0 numpy~=2.3.4 flask==3.0.0 flask-cors==4.0.0 pillow>=10.4.0
```

### Frontend zeigt "Backend offline"?
1. Starte `start_backend.bat` zuerst
2. Warte bis "Running on http://127.0.0.1:5000"
3. Dann starte `start_frontend.bat`

### Modell nicht gefunden?
```bash
# Trainiere das Modell:
python NN_Model.py

# Erstellt: mnist_model.keras
```

### Port 5000 bereits belegt?
In `app.py` ändere:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

In `frontend/app.js` ändere:
```javascript
BACKEND_URL: 'http://localhost:5001'
```


## Nächste Schritte

### Modell verbessern
1. Öffne `NN_Model.py`
2. Ändere Architektur (Layers, Dropout, etc.)
3. Führe aus: `python NN_Model.py`
4. Neues Modell wird gespeichert

### Design anpassen
1. Öffne `frontend/styles.css`
2. Ändere CSS-Variablen `:root`
3. Speichern & Browser neu laden (F5)

### Deployment
- Backend: Flask + Gunicorn auf Server
- Frontend: Static Hosting (Netlify, Vercel)
- Oder: Docker Container


## Support

Bei Problemen:
1. Prüfe Browser Console (F12)
2. Prüfe Terminal-Output
3. Checke README.md für Details


## License
MIT - Frei verwendbar für eigene Projekte!


---
Erstellt mit ❤️ und KI

