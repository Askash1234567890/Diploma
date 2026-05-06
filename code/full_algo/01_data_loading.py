"""
Step 1: Import libraries, load data, compute normalized harmonic ratios.

Outputs (saved to module-level variables for subsequent steps):
    df       — merged DataFrame with shape params and normalized harmonic ratios
    x_mean   — feature mean used for standardization
    x_std    — feature std used for standardization
"""

import warnings
import zipfile

import numpy as np
import pandas as pd
from joblib import dump, load
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import r2_score
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from tqdm import tqdm

warnings.filterwarnings("ignore")
pd.set_option("display.precision", 15)

rs = 42

# Unpack pre-trained models (skip if training from scratch)
with zipfile.ZipFile("../../trained_models_and_other_zip_files/models_2.zip", "r") as zf:
    zf.extractall()

shape = pd.read_csv("../../data/shape.csv")
gradient = pd.read_csv("../../data/gradients.csv", index_col="ts")

df = shape.merge(gradient, how="inner", on="id")

# Normalized harmonic ratios — suppress h6, h10, h14 simultaneously
df["h6/h2"]  = df["h6"]  / df["h2"]
df["h10/h2"] = df["h10"] / df["h2"]
df["h14/h2"] = df["h14"] / df["h2"]

for col in ["h6/h2", "h10/h2", "h14/h2"]:
    df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

print(df[["Rightchamfer", "Leftchamfer", "h6/h2", "h10/h2", "h14/h2"]].sample(5))
