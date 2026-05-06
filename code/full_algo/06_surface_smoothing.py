"""
Step 6: Smooth the 32×32 simulation grid to 500×500 using the trained
SVR ensemble.  Saves svr_h6.csv, svr_h10.csv, svr_h14.csv.

This step is compute-intensive (~13 min per harmonic on CPU).
Run after 05_model_inference.py (models must be loaded).
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from joblib import load
from tqdm import tqdm
import os, warnings

warnings.filterwarnings("ignore")

N_folds   = 10
MODEL_DIR = "models_svr_2"
OUT_DIR   = "exetended_harmonic_data"
os.makedirs(OUT_DIR, exist_ok=True)

shape    = pd.read_csv("../../data/shape.csv")
gradient = pd.read_csv("../../data/gradients.csv", index_col="ts")
df = shape.merge(gradient, how="inner", on="id")

x_mean = df[["Rightchamfer", "Leftchamfer"]].mean()
x_std  = df[["Rightchamfer", "Leftchamfer"]].std()

models_h6  = [load(f"{MODEL_DIR}/models_h6/model_{i}.joblib")  for i in range(1, N_folds + 1)]
models_h10 = [load(f"{MODEL_DIR}/models_h10/model_{i}.joblib") for i in range(1, N_folds + 1)]
models_h14 = [load(f"{MODEL_DIR}/models_h14/model_{i}.joblib") for i in range(1, N_folds + 1)]


def full_predict(models, X):
    preds = np.zeros(X.shape[0])
    for m in models:
        preds += m.predict(np.array(X))
    return preds / N_folds


def build_surface(models, value_col: str, out_csv: str, n_points: int = 500):
    """Query the model ensemble on an n_points × n_points grid and save to CSV."""
    lc_scaled = (np.linspace(df["Leftchamfer"].min(),  df["Leftchamfer"].max(),  n_points) - x_mean["Leftchamfer"])  / x_std["Leftchamfer"]
    rc_scaled = (np.linspace(df["Rightchamfer"].min(), df["Rightchamfer"].max(), n_points) - x_mean["Rightchamfer"]) / x_std["Rightchamfer"]

    rows = []
    for r in tqdm(rc_scaled, desc=f"Building {value_col} surface"):
        for l in lc_scaled:
            pred = full_predict(models, np.array([[r, l]]))[0]
            r_real = r * x_std["Rightchamfer"] + x_mean["Rightchamfer"]
            l_real = l * x_std["Leftchamfer"]  + x_mean["Leftchamfer"]
            rows.append({"Rightchamfer": r_real, "Leftchamfer": l_real, value_col: pred})

    surf = pd.DataFrame(rows)
    surf.to_csv(f"{OUT_DIR}/{out_csv}", index=False)
    print(f"Saved: {OUT_DIR}/{out_csv}")
    return surf


surf_h6  = build_surface(models_h6,  "h6/h2",  "svr_h6.csv")
surf_h10 = build_surface(models_h10, "h10/h2", "svr_h10.csv")
surf_h14 = build_surface(models_h14, "h14/h2", "svr_h14.csv")

# Quick sanity-check heatmap
fig, axes = plt.subplots(1, 3, figsize=(17, 5), constrained_layout=True)
for ax, surf, col in zip(axes,
                         [surf_h6, surf_h10, surf_h14],
                         ["h6/h2", "h10/h2", "h14/h2"]):
    pivot = pd.pivot_table(surf, index="Leftchamfer", columns="Rightchamfer",
                           values=col, aggfunc="mean")
    import seaborn as sns
    sns.heatmap(pivot, ax=ax, cmap="coolwarm", cbar=True)
    ax.set_title(f"SVR surface — {col} (500×500)")
plt.savefig("surfaces_500x500.png", dpi=100)
plt.show()
print("Saved: surfaces_500x500.png")
