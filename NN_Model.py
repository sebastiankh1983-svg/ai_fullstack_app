import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-GUI Backend
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist
from sklearn.metrics import confusion_matrix, classification_report
import datetime
import argparse
import os

def log_status(msg):
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    try:
        with open('training_status.log', 'a', encoding='utf-8') as f:
            f.write(line + '\n')
    except Exception:
        pass
    print(line, flush=True)

log_status("Start Training Skript")
print("MNIST Model Training Script Loaded")
log_status("Skript geladen, beginne Argument Parsing")

parser = argparse.ArgumentParser(description="Trainiere MNIST Modell (Dense oder CNN)")
parser.add_argument('--epochs', type=int, default=20, help='Anzahl Epochen')
parser.add_argument('--batch', type=int, default=128, help='Batchgröße')
parser.add_argument('--model-type', choices=['dense', 'cnn'], default='cnn', help='Modelltyp wählen')
parser.add_argument('--lr', type=float, default=0.001, help='Learning Rate')
parser.add_argument('--augment', action='store_true', help='Aktiviere Data Augmentation (nur für CNN sinnvoll)')
parser.add_argument('--patience', type=int, default=5, help='EarlyStopping Geduld')
parser.add_argument('--tag', type=str, default='', help='Optionaler Tag für Dateinamen')
args = parser.parse_args()

print(f"Konfiguration: epochs={args.epochs}, batch={args.batch}, lr={args.lr}, type={args.model_type}, augment={args.augment}")
log_status("Konfiguration eingelesen")

#1 Daten laden
(x_train, y_train), (x_test, y_test) = mnist.load_data()
log_status("MNIST Daten geladen")
print(f"Training: {len(x_train)} Bilder, Test: {len(x_test)} Bilder")

# Normalisierung der Daten
x_train = x_train.astype("float32") / 255.0
x_test = x_test.astype("float32") / 255.0

# Für CNN Kanal-Dimension hinzufügen
if args.model_type == 'cnn':
    x_train = np.expand_dims(x_train, -1)  # (N,28,28,1)
    x_test = np.expand_dims(x_test, -1)
    log_status("Kanal-Dimension hinzugefügt für CNN")

plt.imshow(x_train[0].squeeze(), cmap='gray')
plt.title(f"Sample Label {y_train[0]}")
plt.savefig('training_image.png')
plt.close()

#2 Modell erstellen (wahlweise Dense oder CNN)
if args.model_type == 'dense':
    model = keras.Sequential([
        layers.Flatten(input_shape=(28, 28)),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(10, activation='softmax')
    ])
else:
    # CNN Modell für bessere Generalisierung
    inputs = keras.Input(shape=(28, 28, 1))
    x = layers.Conv2D(32, 3, activation='relu')(inputs)
    x = layers.BatchNormalization()(x)
    x = layers.Conv2D(64, 3, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Dropout(0.25)(x)
    x = layers.Conv2D(128, 3, activation='relu')(x)
    x = layers.BatchNormalization()(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Dropout(0.25)(x)
    x = layers.Flatten()(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(10, activation='softmax')(x)
    model = keras.Model(inputs, outputs)

print(model.summary())
log_status("Modell erstellt")

# Optional Data Augmentation
train_data = None
if args.augment and args.model_type == 'cnn':
    datagen = keras.preprocessing.image.ImageDataGenerator(
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1
    )
    datagen.fit(x_train)
    train_data = datagen.flow(x_train, y_train, batch_size=args.batch)
    log_status("Data Augmentation aktiviert")

#3 Modell kompilieren
optimizer = keras.optimizers.Adam(learning_rate=args.lr)
model.compile(optimizer=optimizer,
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy']
              )
print("Modell kompiliert")
log_status("Modell kompiliert")

# Callbacks
callbacks = [
    keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=args.patience, restore_best_weights=True),
    keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, verbose=1)
]

#4 Modell trainieren
log_status("Starte Training")
if train_data:
    history = model.fit(train_data, epochs=args.epochs, validation_data=(x_test, y_test), verbose=1, callbacks=callbacks)
else:
    history = model.fit(x_train, y_train, epochs=args.epochs, batch_size=args.batch, validation_split=0.1, verbose=1, callbacks=callbacks)
print("Modell trainiert")
log_status("Training abgeschlossen (raw)")

#5 Modell evaluieren
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=1)
print(f"Test accuracy: {test_acc:.4f}")
log_status(f"Evaluation abgeschlossen: acc={test_acc:.4f}")

#6 Modell speichern (mit Zeitstempel)
stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
base_name = 'mnist_model'
if args.tag:
    base_name += f"_{args.tag}"
file_name = f"{base_name}_{args.model_type}_{stamp}.keras"
model.save(file_name)
print(f"Modell gespeichert als {file_name}")
log_status(f"Gespeichert: {file_name} & mnist_model.keras aktualisiert")
# Zusätzlich aktuelles Standardmodell überschreiben
model.save('mnist_model.keras')
print("Standardmodell aktualisiert: mnist_model.keras")
log_status("Standardmodell aktualisiert")

#7 Vorhersagen machen
predictions = model.predict(x_test)
predicted_labels = np.argmax(predictions, axis=1)
print(f"Vorhersagen für die ersten 5 Testbilder: {predicted_labels[:5]}")
print(f"Tatsächliche Labels für die ersten 5 Testbilder: {y_test[:5]}")
log_status("Vorhersagen für die ersten 5 Testbilder gemacht")

#8 Einige Vorhersagen visualisieren
num_images = 8
plt.figure(figsize=(12, 4))
for i in range(num_images):
    plt.subplot(2, 4, i+1)
    plt.imshow(x_test[i].squeeze(), cmap='gray')
    plt.title(f"Pred: {predicted_labels[i]}\nTrue: {y_test[i]}")
    plt.axis('off')
plt.tight_layout()
plt.savefig('predictions_visualization.png')
plt.close()
print("Vorhersagen visualisiert und gespeichert")
log_status("Vorhersage-Visualisierung fertig")

#9 Confusion Matrix
cm = confusion_matrix(y_test, predicted_labels)
plt.figure(figsize=(6,6))
plt.imshow(cm, cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, cm[i, j], ha='center', va='center', color='red', fontsize=8)
plt.tight_layout()
plt.savefig('confusion_matrix.png')
plt.close()
print("Confusion Matrix gespeichert als confusion_matrix.png")
log_status("Confusion Matrix fertig")

#10 Classification Report
report = classification_report(y_test, predicted_labels)
with open('classification_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)
print("Classification Report gespeichert (classification_report.txt)")
log_status("Classification Report geschrieben")

#11 Trainingskurven speichern
if 'accuracy' in history.history:
    plt.figure(figsize=(10,4))
    plt.subplot(1,2,1)
    plt.plot(history.history['accuracy'], label='train_acc')
    plt.plot(history.history.get('val_accuracy', []), label='val_acc')
    plt.title('Accuracy')
    plt.legend()
    plt.subplot(1,2,2)
    plt.plot(history.history['loss'], label='train_loss')
    plt.plot(history.history.get('val_loss', []), label='val_loss')
    plt.title('Loss')
    plt.legend()
    plt.tight_layout()
    plt.savefig('training_curves.png')
    plt.close()
    print("Trainingskurven gespeichert (training_curves.png)")
    log_status("Trainingskurven gespeichert")

log_status("Skript Ende")
print("Training abgeschlossen.")
