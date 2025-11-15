import os

# HTML Content
html_content = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Development App</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>AI Development Application</h1>
            <p>Full Stack AI Development</p>
        </header>
        <main>
            <section id="app"></section>
        </main>
    </div>
    <script src="app.js"></script>
</body>
</html>"""

# CSS Content
css_content = """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.container {
    background: white;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    max-width: 1100px;
    width: 100%;
    padding: 40px;
}

header {
    text-align: center;
    margin-bottom: 40px;
    border-bottom: 2px solid #667eea;
    padding-bottom: 20px;
}

header h1 {
    color: #333;
    margin-bottom: 10px;
    font-size: 2.5em;
}

header p {
    color: #666;
    font-size: 1.1em;
}

main {
    min-height: 400px;
}

section {
    margin: 20px 0;
}

button {
    background-color: #667eea;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1em;
    transition: background-color 0.3s;
    margin-right: 10px;
    margin-bottom: 10px;
}

button:hover {
    background-color: #764ba2;
}

input[type="file"],
input[type="text"],
textarea {
    width: 100%;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-family: inherit;
}

.prediction-container {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 30px;
    margin-top: 20px;
}

.prediction-result {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 30px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.prediction-number {
    font-size: 4em;
    font-weight: bold;
    margin: 20px 0;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.confidence-text {
    font-size: 1.2em;
    margin-top: 10px;
}

.chart-container {
    background: white;
    padding: 20px;
    border-radius: 10px;
    border: 1px solid #e0e0e0;
}

.chart-title {
    font-size: 1.3em;
    color: #333;
    margin-bottom: 20px;
    font-weight: 600;
}

.bar-chart {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.bar-item {
    display: flex;
    align-items: center;
    gap: 10px;
}

.bar-label {
    min-width: 60px;
    font-weight: 600;
    color: #333;
    font-size: 0.95em;
}

.bar-wrapper {
    flex: 1;
    background: #f0f0f0;
    border-radius: 5px;
    height: 30px;
    position: relative;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    border-radius: 5px;
    transition: width 0.6s ease-out;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding-right: 8px;
    color: white;
    font-weight: 600;
    font-size: 0.85em;
}

.bar-fill.top-prediction {
    background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
}

.bar-value {
    min-width: 60px;
    text-align: right;
    font-weight: 600;
    color: #666;
    font-size: 0.9em;
}

.image-preview {
    margin: 20px 0;
    text-align: center;
}

.image-preview img {
    max-width: 200px;
    max-height: 200px;
    border: 2px solid #667eea;
    border-radius: 5px;
    padding: 10px;
    background: white;
}

.error {
    background-color: #ffe5e5;
    color: #d32f2f;
    padding: 15px;
    border-radius: 5px;
    margin: 10px 0;
    border-left: 4px solid #d32f2f;
}

.loading {
    text-align: center;
    padding: 20px;
    font-size: 1.2em;
    color: #667eea;
}

.loading::after {
    content: "...";
    animation: dots 1.5s steps(4, end) infinite;
}

@keyframes dots {
    0%, 20% { content: "."; }
    40% { content: ".."; }
    60%, 100% { content: "..."; }
}

@media (max-width: 768px) {
    .container {
        padding: 20px;
    }
    header h1 {
        font-size: 1.8em;
    }
    .prediction-container {
        grid-template-columns: 1fr;
    }
}"""

# JavaScript Content
js_content = """document.addEventListener('DOMContentLoaded', function() {
    console.log('App loaded');
    const appSection = document.getElementById('app');
    loadMainPage();
});

function loadMainPage() {
    const appSection = document.getElementById('app');
    appSection.innerHTML = `
        <div class="main-content">
            <h2>Willkommen zur AI Application</h2>
            <p>Dies ist die Frontend-Anwendung für Ihr Full-Stack AI Development Projekt.</p>
            <button onclick="loadMnistPage()">MNIST Modell</button>
            <button onclick="loadInfoPage()">Informationen</button>
        </div>
    `;
}

function loadMnistPage() {
    const appSection = document.getElementById('app');
    appSection.innerHTML = `
        <div class="mnist-section">
            <h2>MNIST Handschriftenerkennung</h2>
            <p>Laden Sie ein Bild hoch um die Vorhersage zu testen:</p>
            <input type="file" id="mnistFile" accept="image/*" onchange="previewImage(event)">
            <div id="imagePreview" class="image-preview"></div>
            <button onclick="predictMnist()">Vorhersage</button>
            <div id="mnistResult"></div>
            <button onclick="loadMainPage()" style="margin-top: 20px;">Zurück</button>
        </div>
    `;
}

function previewImage(event) {
    const file = event.target.files[0];
    const previewDiv = document.getElementById('imagePreview');

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewDiv.innerHTML = `
                <h3>Bildvorschau:</h3>
                <img src="${e.target.result}" alt="Vorschau">
            `;
        };
        reader.readAsDataURL(file);
    }
}

function predictMnist() {
    const fileInput = document.getElementById('mnistFile');
    const resultDiv = document.getElementById('mnistResult');

    if (!fileInput.files.length) {
        resultDiv.innerHTML = '<div class="error">Bitte wählen Sie ein Bild aus.</div>';
        return;
    }

    resultDiv.innerHTML = '<div class="loading">Analysiere Bild mit KI-Modell</div>';

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('http://localhost:5000/api/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            displayPredictionResult(data);
        } else {
            resultDiv.innerHTML = `<div class="error">Fehler: ${data.error}</div>`;
        }
    })
    .catch(error => {
        resultDiv.innerHTML = `<div class="error">Fehler beim Verbinden mit dem Backend: ${error.message}<br><small>Stellen Sie sicher, dass das Backend auf Port 5000 läuft.</small></div>`;
    });
}

function displayPredictionResult(data) {
    const resultDiv = document.getElementById('mnistResult');
    const probabilities = data.probabilities;

    let barsHTML = '';
    for (let i = 0; i < 10; i++) {
        const prob = probabilities[i.toString()] || 0;
        const isTopPrediction = i === data.prediction;
        barsHTML += `
            <div class="bar-item">
                <div class="bar-label">Ziffer ${i}:</div>
                <div class="bar-wrapper">
                    <div class="bar-fill ${isTopPrediction ? 'top-prediction' : ''}"
                         style="width: ${prob}%">
                        ${prob > 10 ? prob.toFixed(1) + '%' : ''}
                    </div>
                </div>
                <div class="bar-value">${prob.toFixed(1)}%</div>
            </div>
        `;
    }

    resultDiv.innerHTML = `
        <div class="prediction-container">
            <div class="prediction-result">
                <h3>🎯 Vorhersage</h3>
                <div class="prediction-number">${data.prediction}</div>
                <div class="confidence-text">
                    Konfidenz: <strong>${data.confidence}%</strong>
                </div>
                <p style="margin-top: 15px; font-size: 0.9em; opacity: 0.9;">
                    Das Modell ist zu ${data.confidence}% sicher, dass dies eine ${data.prediction} ist.
                </p>
            </div>
            <div class="chart-container">
                <div class="chart-title">📊 Wahrscheinlichkeitsverteilung</div>
                <div class="bar-chart">
                    ${barsHTML}
                </div>
            </div>
        </div>
    `;
}

function loadInfoPage() {
    const appSection = document.getElementById('app');
    appSection.innerHTML = `
        <div class="info-section">
            <h2>Informationen</h2>
            <p><strong>Projekt:</strong> Full Stack AI Development</p>
            <p><strong>Technologien:</strong></p>
            <ul>
                <li>Frontend: HTML5, CSS3, JavaScript</li>
                <li>Backend: Python Flask</li>
                <li>ML: TensorFlow/Keras</li>
            </ul>
            <button onclick="loadMainPage()" style="margin-top: 20px;">Zurück</button>
        </div>
    `;
}"""

# Write files
base_path = r'C:\Users\sebas\PycharmProjects\Full_Stack_Ai_Development\frontend\public'

with open(os.path.join(base_path, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html_content)

with open(os.path.join(base_path, 'styles.css'), 'w', encoding='utf-8') as f:
    f.write(css_content)

with open(os.path.join(base_path, 'app.js'), 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Alle Dateien erfolgreich erstellt!")

