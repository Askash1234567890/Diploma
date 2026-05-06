"""
Step 2: Exploratory analysis — heatmaps of h6/h2, h10/h2, h14/h2
over the (Rightchamfer, Leftchamfer) parameter space.

Run after 01_data_loading.py (df must be in scope).
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from01_data_loading import df  # noqa: F401  (run standalone: exec 01 first)


def plot_heatmap(df, ax, x_axis, y_axis, title, ticks_on_map, include_scale=True):
    sns.heatmap(
        df,
        ax=ax,
        cmap="coolwarm",
        xticklabels=x_axis,
        yticklabels=y_axis,
        cbar=include_scale,
    )
    ax.set_title(title)
    _reset_axes(ax, df.shape[0] // ticks_on_map, df.shape[1] // ticks_on_map)


def _reset_axes(ax, skip_x, skip_y):
    ax.set_xticks(ax.get_xticks()[::skip_x])
    ax.set_yticks(ax.get_yticks()[::skip_y])


pivot_h6  = pd.pivot_table(df, index="Leftchamfer", columns="Rightchamfer", values="h6/h2",  aggfunc="mean")
pivot_h10 = pd.pivot_table(df, index="Leftchamfer", columns="Rightchamfer", values="h10/h2", aggfunc="mean")
pivot_h14 = pd.pivot_table(df, index="Leftchamfer", columns="Rightchamfer", values="h14/h2", aggfunc="mean")

ticks_on_map = 15
round_values  = 2
x_axis = np.round(np.linspace(0, 10, pivot_h6.shape[0]), round_values)
y_axis = np.round(np.linspace(0, 20, pivot_h6.shape[1]), round_values)

fig, axes = plt.subplots(1, 3, figsize=(17, 5), constrained_layout=True)
plot_heatmap(pivot_h6,  axes[0], x_axis, y_axis, "h6/h2",  ticks_on_map)
plot_heatmap(pivot_h10, axes[1], x_axis, y_axis, "h10/h2", ticks_on_map)
plot_heatmap(pivot_h14, axes[2], x_axis, y_axis, "h14/h2", ticks_on_map)
plt.suptitle("Raw simulation harmonics heatmaps (32×32 grid)")
plt.savefig("heatmaps_raw.png", dpi=150)
plt.show()
print("Saved: heatmaps_raw.png")
