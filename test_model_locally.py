"""
Lokaler Test des trainierten Modells mit MNIST-Testdaten
"""
import numpy as np
from tensorflow import keras
from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt

# Modell laden
print("Lade Modell...")
model = keras.models.load_model('mnist_model.keras')
print("✓ Modell geladen\n")

# MNIST Test-Daten laden
(_, _), (x_test, y_test) = mnist.load_data()

# Daten vorbereiten (genau wie im Training)
x_test = x_test.astype("float32") / 255.0
x_test = np.expand_dims(x_test, -1)  # (N, 28, 28, 1)

print("Teste 10 zufällige Bilder...\n")

# 10 zufällige Indizes
random_indices = np.random.choice(len(x_test), 10, replace=False)

correct = 0
for idx in random_indices:
    # Vorhersage
    img = x_test[idx:idx+1]  # (1, 28, 28, 1)
    pred = model.predict(img, verbose=0)
    predicted_digit = np.argmax(pred[0])
    confidence = pred[0][predicted_digit]
    actual = y_test[idx]

    is_correct = predicted_digit == actual
    if is_correct:
        correct += 1

    status = "✓" if is_correct else "✗"
    print(f"{status} Bild #{idx}: Vorhersage={predicted_digit} (Konfidenz: {confidence:.2%}), Tatsächlich={actual}")

print(f"\n{'='*60}")
print(f"Genauigkeit: {correct}/10 = {correct/10:.0%}")
print(f"{'='*60}")

# Visualisierung der ersten 5 Fehler (falls vorhanden)
print("\nSuche nach Fehlern in den ersten 100 Testbildern...")
errors = []
for i in range(100):
    img = x_test[i:i+1]
    pred = model.predict(img, verbose=0)
    predicted = np.argmax(pred[0])
    actual = y_test[i]
    if predicted != actual:
        errors.append((i, predicted, actual, pred[0]))

if errors:
    print(f"Gefunden: {len(errors)} Fehler\n")

    # Visualisiere erste 5 Fehler
    n_show = min(5, len(errors))
    plt.figure(figsize=(15, 3))
    for i, (idx, pred, actual, probs) in enumerate(errors[:n_show]):
        plt.subplot(1, n_show, i+1)
        plt.imshow(x_test[idx].squeeze(), cmap='gray')
        plt.title(f"Pred: {pred} ({probs[pred]:.1%})\nActual: {actual}", fontsize=10)
        plt.axis('off')

    plt.tight_layout()
    plt.savefig('model_errors.png')
    print("✓ Fehler-Visualisierung gespeichert: model_errors.png")
else:
    print("✓ Keine Fehler in den ersten 100 Testbildern gefunden!")

# Gesamtauswertung
print("\n" + "="*60)
print("Vollständige Evaluation auf allen 10.000 Testbildern...")
print("="*60)
loss, acc = model.evaluate(x_test, y_test, verbose=0)
print(f"Test-Loss: {loss:.4f}")
print(f"Test-Accuracy: {acc:.4%}")
print("="*60)

