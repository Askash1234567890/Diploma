"""
Step 7: Gradient descent on shape parameters using the SVR ensemble as a
differentiable surrogate loss.

Gradient is computed numerically (finite differences) since SVR has no
analytical autodiff.  At convergence the optimal (Rightchamfer, Leftchamfer)
are printed for use in make_1_script.py.

Run after 05_model_inference.py.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from joblib import load
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore")

N_folds   = 10
MODEL_DIR = "models_svr_2"

shape    = pd.read_csv("../../data/shape.csv")
gradient = pd.read_csv("../../data/gradients.csv", index_col="ts")
df = shape.merge(gradient, how="inner", on="id")

x_mean = df[["Rightchamfer", "Leftchamfer"]].mean()
x_std  = df[["Rightchamfer", "Leftchamfer"]].std()

models_h6  = [load(f"{MODEL_DIR}/models_h6/model_{i}.joblib")  for i in range(1, N_folds + 1)]
models_h10 = [load(f"{MODEL_DIR}/models_h10/model_{i}.joblib") for i in range(1, N_folds + 1)]
models_h14 = [load(f"{MODEL_DIR}/models_h14/model_{i}.joblib") for i in range(1, N_folds + 1)]
all_models = [models_h6, models_h10, models_h14]


def full_predict(models, X):
    preds = np.zeros(X.shape[0])
    for m in models:
        preds += m.predict(np.array(X))
    return preds / N_folds


def loss(x):
    """Sum of normalized harmonic predictions + |h6 - h10| penalty."""
    y = np.zeros(x.shape[0])
    for mods in all_models:
        y += full_predict(mods, x)
    y += abs(full_predict(models_h6, x) - full_predict(models_h10, x))
    return y


def numerical_gradient(x, eps=1e-5):
    """Finite-difference gradient of loss w.r.t. both input dimensions."""
    g = np.zeros_like(x)
    for dim in range(x.shape[1]):
        dx = np.zeros_like(x)
        dx[0, dim] = eps
        for mods in all_models:
            pred = full_predict(mods, x)
            g[0, dim] += ((full_predict(mods, x + dx) - pred) / eps * np.sign(pred))[0]
    return g


# Starting point (in original units, converted to standardized space)
start_r, start_l = 2.0, 18.0
x = ((np.array([[start_r, start_l]]) - x_mean.values) / x_std.values)

lr = 1e-2
n_epochs = 1000
loss_hist = [loss(x).flatten()[0]]
shape_history = []

for epoch in tqdm(range(n_epochs), desc="Gradient descent"):
    if epoch > 0 and epoch % 1000 == 0:
        lr /= 3
    grad = numerical_gradient(x)
    x = x - lr * grad
    loss_hist.append(loss(x).flatten()[0])
    shape_history.append((x * x_std.values + x_mean.values).flatten().tolist())

    if epoch % 100 == 0:
        r_now, l_now = (x * x_std.values + x_mean.values).flatten()
        print(f"  epoch {epoch:4d}  loss={loss_hist[-1]:.6f}  R={r_now:.4f}  L={l_now:.4f}")

right, left = (x * x_std.values + x_mean.values).flatten()
print(f"\nOptimized shape:  Rightchamfer={right:.6f}  Leftchamfer={left:.6f}")
print(f"Final loss: {loss_hist[-1]:.6f}")

# Compare against brute-force
bf_r, bf_l = 2.9032967741935485, 15.483893548387096
bf_loss = loss(((np.array([[bf_r, bf_l]]) - x_mean.values) / x_std.values))[0]
print(f"Brute-force loss: {bf_loss:.6f}")
print(f"Improvement: {(1 - loss_hist[-1] / bf_loss) * 100:.2f}%")

plt.figure(figsize=(10, 4))
plt.plot(loss_hist)
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.title("Gradient descent convergence")
plt.grid()
plt.tight_layout()
plt.savefig("gradient_descent_loss.png", dpi=150)
plt.show()
print("Saved: gradient_descent_loss.png")
