"""
Step 8: Final visualization — smoothed 500×500 heatmaps with brute-force
and gradient-descent result points overlaid.  Also plots |B| and B_θ
from Opera field files for the presentation.

Run after 06_surface_smoothing.py and 07_gradient_descent.py.
"""

import zipfile
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ── load smoothed surfaces ───────────────────────────────────────────────────
OUT_DIR = "exetended_harmonic_data"
df_h6  = pd.read_csv(f"{OUT_DIR}/svr_h6.csv")
df_h10 = pd.read_csv(f"{OUT_DIR}/svr_h10.csv")
df_h14 = pd.read_csv(f"{OUT_DIR}/svr_h14.csv")

for df_s, col in [(df_h6, "h6/h2"), (df_h10, "h10/h2"), (df_h14, "h14/h2")]:
    df_s[col] = (df_s[col] - df_s[col].min()) / (df_s[col].max() - df_s[col].min())

pivot_h6  = pd.pivot_table(df_h6,  index="Leftchamfer", columns="Rightchamfer", values="h6/h2",  aggfunc="mean")
pivot_h10 = pd.pivot_table(df_h10, index="Leftchamfer", columns="Rightchamfer", values="h10/h2", aggfunc="mean")
pivot_h14 = pd.pivot_table(df_h14, index="Leftchamfer", columns="Rightchamfer", values="h14/h2", aggfunc="mean")

# ── reference points ─────────────────────────────────────────────────────────
# Brute-force best from the 32×32 grid
rightchamfer_raw, leftchamfer_raw = 2.9032967741935485, 15.483893548387096
# ML gradient descent result
right, left = 2.938228798088884, 16.19596210921747

def _snap(pivot, r, l):
    r_snap = pivot.columns[abs(pivot.columns - r).argmin()]
    l_snap = pivot.index[abs(pivot.index   - l).argmin()]
    return r_snap, l_snap


def plot_heatmap(df, ax, title, ticks=15, include_scale=True):
    n = df.shape[0]
    x_axis = np.round(np.linspace(0, 10, n), 2)
    y_axis = np.round(np.linspace(0, 20, n), 2)
    sns.heatmap(df, ax=ax, cmap="coolwarm",
                xticklabels=x_axis, yticklabels=y_axis, cbar=include_scale)
    ax.set_title(title)
    skip = n // ticks
    ax.set_xticks(ax.get_xticks()[::skip])
    ax.set_yticks(ax.get_yticks()[::skip])


def plot_point(pivot, ax, r, l, label, color):
    col_idx = pivot.columns.get_loc(_snap(pivot, r, l)[0])
    row_idx = pivot.index.get_loc(_snap(pivot, r, l)[1])
    ax.scatter([col_idx], [row_idx], color=color, s=25, label=label)
    ax.legend(loc="upper right", fontsize=7)


fig, axes = plt.subplots(1, 3, figsize=(16, 5), constrained_layout=True)
for ax, pivot, col in zip(axes,
                           [pivot_h6, pivot_h10, pivot_h14],
                           ["h6/h2", "h10/h2", "h14/h2"]):
    plot_heatmap(pivot, ax, col, include_scale=(ax is axes[2]))
    plot_point(pivot, ax, rightchamfer_raw, leftchamfer_raw, "Brute-force optimum", "black")
    plot_point(pivot, ax, right, left, "ML gradient descent", "orange")

plt.suptitle("Smoothed harmonic maps (500×500) — result comparison", fontsize=13)
plt.savefig("result_comparison.png", dpi=150)
plt.show()
print("Saved: result_comparison.png")

# ── magnetic field plots ──────────────────────────────────────────────────────
with zipfile.ZipFile("../../trained_models_and_other_zip_files/fields_data.zip", "r") as zf:
    zf.extractall("fields_data")


def read_field_file(path):
    with open(path, "r", encoding="utf-8") as f:
        cols = f.readline().strip().split()
        data = [list(map(float, line.strip().split())) for line in f]
    return pd.DataFrame(data, columns=cols)


df_nonopt = read_field_file("fields_data/Магнитное_поле_неидеальной_формы.txt")
df_theta  = read_field_file("fields_data/Тангенсальная_компонента_неидеального_поля.txt")
df_opt    = read_field_file("fields_data/Поле_идеальной_формы.txt")

angle = np.linspace(0, 360, len(df_nonopt))

fig, axes = plt.subplots(1, 3, figsize=(18, 5), constrained_layout=True)

axes[0].plot(angle, df_nonopt["B"], linewidth=2)
axes[0].set_title("|B| — non-optimal shape")
axes[0].set_xlabel("Angle (°)"); axes[0].set_ylabel("|B|"); axes[0].grid()

axes[1].plot(np.linspace(0, 360, len(df_theta)), df_theta["BT"], linewidth=2, color="darkorange")
axes[1].set_title("B_θ — non-optimal shape")
axes[1].set_xlabel("Angle (°)"); axes[1].set_ylabel("B_θ"); axes[1].grid()

axes[2].plot(np.linspace(0, 360, len(df_opt)), df_opt["B"], linewidth=2, color="green")
axes[2].set_title("|B| — optimized shape")
axes[2].set_xlabel("Angle (°)"); axes[2].set_ylabel("|B|"); axes[2].grid()

plt.suptitle("Magnetic field on the reference circle", fontsize=13)
plt.savefig("field_comparison.png", dpi=150)
plt.show()
print("Saved: field_comparison.png")
