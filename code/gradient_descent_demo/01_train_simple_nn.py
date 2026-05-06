"""
Step 1: Train a minimal neural network on synthetic data.

This is a proof-of-concept that validates the gradient descent on features
idea before applying it to the real SVR-based surrogate model.

The network has a single dense layer (linear activation), so the loss surface
is quadratic and gradient descent converges cleanly — a sanity check.

Saves: simple_nn_model/  (Keras SavedModel format)
"""

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model

np.random.seed(42)
tf.random.set_seed(42)

N = 3
x = np.array([
    [np.random.randint(i + N) * np.random.randint(j + N) for i in range(N)]
    for j in range(N)
], dtype=np.float32)
y = np.array([np.random.randint(N) for _ in range(N)], dtype=np.float32)

print("Training data:")
print("  x =", x)
print("  y =", y)

inp = Input(shape=[x.shape[1]])
out = Dense(1, activation="linear")(inp)
model = Model(inp, out)
model.compile(optimizer="adam", loss="mse")

history = model.fit(x, y, epochs=100, verbose=0)

print("\nModel summary:")
model.summary()
print("\nLearned weights:", model.get_weights())
print(f"Final training loss: {history.history['loss'][-1]:.6f}")

model.save("simple_nn_model")
print("Model saved to: simple_nn_model/")

plt.figure(figsize=(8, 4))
plt.plot(history.history["loss"])
plt.xlabel("Epoch")
plt.ylabel("MSE loss")
plt.title("Training loss — simple NN on synthetic data")
plt.grid()
plt.tight_layout()
plt.savefig("nn_training_loss.png", dpi=150)
plt.show()
print("Saved: nn_training_loss.png")
