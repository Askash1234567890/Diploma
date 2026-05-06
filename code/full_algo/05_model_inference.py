"""
Step 5: Load pre-trained SVR models and evaluate ensemble predictions.

Expects models_svr_2/ directory (from models_2.zip) or models trained in step 4.
Prints R² on the held-out test set and plots residuals.
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from joblib import load
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import warnings

warnings.filterwarnings("ignore")

rs = 42
N_folds = 10
MODEL_DIR = "models_svr_2"   # change to "models_svr" if you trained in step 4

shape    = pd.read_csv("../../data/shape.csv")
gradient = pd.read_csv("../../data/gradients.csv", index_col="ts")
df = shape.merge(gradient, how="inner", on="id")

for col, num, den in [("h6/h2", "h6", "h2"), ("h10/h2", "h10", "h2"), ("h14/h2", "h14", "h2")]:
    df[col] = df[num] / df[den]
    df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

target_name = "h6/h2"
df["_group"] = pd.qcut(df[target_name], N_folds, labels=[f"g{i}" for i in range(N_folds)])

_, df_test_raw, _, y_test = train_test_split(
    df[["Rightchamfer", "Leftchamfer", "_group"]],
    df[target_name],
    test_size=0.2,
    random_state=rs,
    stratify=df["_group"],
)

x_mean = df[["Rightchamfer", "Leftchamfer"]].mean()
x_std  = df[["Rightchamfer", "Leftchamfer"]].std()
df_test = (df_test_raw[["Rightchamfer", "Leftchamfer"]] - x_mean) / x_std


def full_predict(models, X):
    preds = np.zeros(X.shape[0])
    for m in models:
        preds += m.predict(np.array(X))
    return preds / N_folds


models_h6  = [load(f"{MODEL_DIR}/models_h6/model_{i}.joblib")  for i in range(1, N_folds + 1)]
models_h10 = [load(f"{MODEL_DIR}/models_h10/model_{i}.joblib") for i in range(1, N_folds + 1)]
models_h14 = [load(f"{MODEL_DIR}/models_h14/model_{i}.joblib") for i in range(1, N_folds + 1)]

y_pred = full_predict(models_h6, df_test)
print(f"Ensemble R² on test set (h6/h2): {r2_score(y_test, y_pred):.4f}")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
residuals = y_test.values - y_pred
sns.histplot(residuals, kde=True, ax=axes[0])
axes[0].set_title("Residuals distribution (h6/h2)")
axes[0].set_xlabel("y_true − y_pred")

axes[1].scatter(y_test, y_pred, alpha=0.4, s=10)
lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
axes[1].plot(lims, lims, "r--", linewidth=1)
axes[1].set_xlabel("True")
axes[1].set_ylabel("Predicted")
axes[1].set_title("True vs Predicted (h6/h2)")

plt.tight_layout()
plt.savefig("inference_diagnostics.png", dpi=150)
plt.show()
print("Saved: inference_diagnostics.png")
