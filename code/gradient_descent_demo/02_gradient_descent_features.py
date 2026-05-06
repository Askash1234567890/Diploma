"""
Step 2: Gradient descent on *input features* using the trained NN as a surrogate.

Instead of updating model weights, we treat the input x as the optimization
variable and use tf.GradientTape to minimize the squared model output.

This demonstrates the core idea applied in 07_gradient_descent.py:
  - Loss = f(x; fixed_weights)²
  - Optimize x to drive the model prediction toward zero

Also cross-checks the TensorFlow autodiff gradient against a manually computed
analytical gradient to confirm correctness.

Run after 01_train_simple_nn.py.
"""

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tqdm import tqdm

np.random.seed(42)
tf.random.set_seed(42)

model = tf.keras.models.load_model("simple_nn_model")
print("Loaded model weights:", model.get_weights())

# Starting point
N = 3
x_test = np.array([[1, 2, 3]], dtype=np.float32)
x_old  = x_test.copy()

print(f"\nInitial features:    {x_test}")
print(f"Initial prediction:  {model.predict(x_test, verbose=0).flatten()[0]:.6f}")

# ── analytical gradient (for sanity check) ───────────────────────────────────
# For a linear model y = w·x + b, d(y²)/dx_i = 2y·w_i
W = model.get_weights()[0]  # shape (n_features, 1)
y0 = model.predict(x_test, verbose=0).flatten()[0]
analytical_grad = [float(2 * y0 * W[i, 0]) for i in range(N)]
print(f"\nAnalytical gradient: {analytical_grad}")

# ── autodiff gradient descent ─────────────────────────────────────────────────
def loss_fn(x):
    return tf.square(model(x))


lr = 0.01
n_epochs = 1000
loss_hist = [float(model(x_test))]
numeric_grad_epoch1 = None

for epoch in tqdm(range(n_epochs), desc="Gradient descent on features"):
    xx = tf.Variable(tf.convert_to_tensor(x_test, dtype=tf.float32))
    with tf.GradientTape() as tape:
        tape.watch(xx)
        loss_val = loss_fn(xx)
    grads = tape.gradient(loss_val, [xx])
    x_test = x_test - lr * np.array(grads).flatten().reshape(1, N)
    loss_hist.append(float(model(x_test)))

    if epoch == 0:
        numeric_grad_epoch1 = np.array(grads).flatten()

    if epoch % 100 == 0:
        print(f"  epoch {epoch:4d}  loss={loss_hist[-1]:.2e}")

print(f"\nAnalytical gradient (epoch 0): {analytical_grad}")
print(f"Autodiff gradient   (epoch 0): {numeric_grad_epoch1}")
print(f"\nOriginal features:  {x_old}")
print(f"Optimized features: {x_test}")
print(f"Final prediction:   {float(model(x_test)):.2e}  (target: 0)")

plt.figure(figsize=(8, 4))
plt.plot(loss_hist)
plt.xlabel("Epoch")
plt.ylabel("Loss (prediction²)")
plt.title("Gradient descent on input features — loss convergence")
plt.yscale("log")
plt.grid()
plt.tight_layout()
plt.savefig("feature_gd_loss.png", dpi=150)
plt.show()
print("Saved: feature_gd_loss.png")
