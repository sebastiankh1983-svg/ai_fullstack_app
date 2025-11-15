import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-GUI Backend
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist

print("MNIST Model Training Script Loaded")
print("="*60)
#1 Daten laden
(x_train, y_train), (x_test, y_test) = mnist.load_data()
print(f"Trainig: {len(x_train)}Bilder") # Text Interpolation

# Normalisierung der Daten
x_train = x_train.astype("float32") / 255.0
#print(x_train)

x_test = x_test.astype("float32") / 255.0
#print(x_test)



plt.imshow(x_train[0], cmap='gray') # Bild anzeigen
plt.title(f"Training {y_train[0]}")
plt.savefig('training_image.png')
plt.close()



#2 Modell erstellen
model = keras.Sequential([
    layers.Flatten(input_shape=(28, 28)),      # Schicht 1: Input-Schicht
    layers.Dense(256, activation='relu'),      # Schicht 2: Dense (erhöht)
    layers.Dropout(0.3),                       # Schicht 3: Dropout
    layers.Dense(128, activation='relu'),      # Schicht 4: Dense
    layers.Dropout(0.3),                       # Schicht 5: Dropout
    layers.Dense(64, activation='relu'),       # Schicht 6: Dense
    layers.Dropout(0.2),                       # Schicht 7: Dropout
    layers.Dense(10, activation='softmax')     # Output-Schicht (KEIN Dropout!)
])
print(model.summary())

#3 Modell kompilieren
optimizer = keras.optimizers.Adam(learning_rate=0.001)
model.compile(optimizer=optimizer,
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy']
              )
print("Modell kompiliert")
print("="*60)

#4 Modell trainieren
model.fit(x_train, y_train, epochs=20, batch_size=128, validation_split=0.1, verbose=1)
print("Modell trainiert")
print("="*60)

#5 Modell evaluieren
test_loss, test_acc = model.evaluate(x_test, y_test, verbose=1)
print(f"Test accuracy: {test_acc}")
print("="*60)

#6 Modell speichern
model.save("mnist_model.keras")
print("Modell gespeichert als mnist_model.keras")
print("="*60)

#7 Vorhersagen machen
predictions = model.predict(x_test)
predicted_labels = np.argmax(predictions, axis=1)
print(f"Vorhersagen für die ersten 5 Testbilder: {predicted_labels[:5]}")
print(f"Tatsächliche Labels für die ersten 5 Testbilder: {y_test[:5]}")
print("="*60)

#8 Einige Vorhersagen visualisieren
num_images = 5
plt.figure(figsize=(10, 5))
for i in range(num_images):
    plt.subplot(1, num_images, i+1)
    plt.imshow(x_test[i], cmap='gray')
    plt.title(f"Pred: {predicted_labels[i]}\nTrue: {y_test[i]}")
    plt.axis('off')
plt.savefig('predictions_visualization.png')
plt.close()
print("Vorhersagen visualisiert und gespeichert")
print("="*60)


