import tensorflow as tf
print('TensorFlow Version:', tf.__version__)
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(28,28,1)),
    tf.keras.layers.Conv2D(4,3,activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(10,activation='softmax')
])
print('Model built OK')
import numpy as np
x = np.random.rand(2,28,28,1).astype('float32')
logits = model(x)
print('Forward pass OK, shape:', logits.shape)

