"""
Step 3: Find the brute-force optimum on the 32×32 simulation grid.

Scans all 1024 rows and finds the shape parameters that minimize the
sum of normalized h6/h2 + h10/h2 + h14/h2.

Run after 01_data_loading.py.
"""

from tqdm import tqdm

from _shared import df  # populated by 01_data_loading.py


minimum = 10.0
best_row = 0

for i in tqdm(range(len(df)), desc="Brute-force search"):
    row_loss = df["h6/h2"].iloc[i] + df["h10/h2"].iloc[i] + df["h14/h2"].iloc[i]
    if row_loss < minimum:
        minimum = row_loss
        best_row = i

rightchamfer_raw, leftchamfer_raw = df.iloc[best_row][["Rightchamfer", "Leftchamfer"]].values.flatten()

print(f"\nBrute-force optimum:")
print(f"  Rightchamfer = {rightchamfer_raw:.6f}")
print(f"  Leftchamfer  = {leftchamfer_raw:.6f}")
print(f"  Loss         = {minimum:.6f}")
