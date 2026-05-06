"""
Step 4: Train SVR models for h6/h2, h10/h2, h14/h2 using 10-fold
stratified cross-validation.  Saves model files to models_svr/.

Run after 01_data_loading.py.
"""

import numpy as np
import pandas as pd
from joblib import dump
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.svm import SVR
from sklearn.metrics import r2_score

# ── reproduced from 01_data_loading.py ──────────────────────────────────────
import warnings, zipfile
warnings.filterwarnings("ignore")
import sys; sys.path.insert(0, "..")
from full_algo._shared import df  # noqa

rs = 42
N_folds = 10

# ── helper ───────────────────────────────────────────────────────────────────
import os
os.makedirs("models_svr/models_h6",  exist_ok=True)
os.makedirs("models_svr/models_h10", exist_ok=True)
os.makedirs("models_svr/models_h14", exist_ok=True)


def train_svr_kfold(target_name: str, svr_params: dict, save_dir: str):
    """Train SVR with stratified KFold and save each fold's model."""
    df["_group"] = pd.qcut(df[target_name], N_folds,
                           labels=[f"g{i}" for i in range(N_folds)])

    df_train, df_test, y_train_full, y_test = train_test_split(
        df[["Rightchamfer", "Leftchamfer", "_group"]],
        df[target_name],
        test_size=0.2,
        random_state=rs,
        stratify=df["_group"],
    )

    x_mean = df_train[["Rightchamfer", "Leftchamfer"]].mean()
    x_std  = df_train[["Rightchamfer", "Leftchamfer"]].std()

    X = (df_train[["Rightchamfer", "Leftchamfer"]] - x_mean) / x_std
    X = pd.concat([X, df_train["_group"]], axis=1)
    X_test = (df_test[["Rightchamfer", "Leftchamfer"]] - x_mean) / x_std

    skf = StratifiedKFold(n_splits=N_folds, shuffle=True, random_state=rs)
    scores, models = [], []

    for fold, (train_idx, val_idx) in enumerate(skf.split(X, X["_group"]), 1):
        X_tr = X.drop(columns=["_group"]).iloc[train_idx].values
        X_val = X.drop(columns=["_group"]).iloc[val_idx].values
        y_tr  = y_train_full.iloc[train_idx]
        y_val = y_train_full.iloc[val_idx]

        model = SVR(**svr_params)
        model.fit(X_tr, y_tr)
        score = r2_score(y_val, model.predict(X_val))
        scores.append(score)
        models.append(model)
        dump(model, f"{save_dir}/model_{fold}.joblib")
        print(f"  Fold {fold}/{N_folds}  R² = {score:.4f}")

    scores = np.array(scores)
    print(f"  Mean R² = {scores.mean():.4f}  ±{scores.std():.4f}\n")
    return models, x_mean, x_std


print("=== h6/h2 ===")
models_h6, x_mean, x_std = train_svr_kfold(
    "h6/h2",
    {"kernel": "rbf", "C": 10, "epsilon": 0.0001, "gamma": 8.5},
    "models_svr/models_h6",
)

print("=== h10/h2 ===")
models_h10, _, _ = train_svr_kfold(
    "h10/h2",
    {"kernel": "rbf", "C": 10, "epsilon": 0.0001, "gamma": 8.6},
    "models_svr/models_h10",
)

print("=== h14/h2 ===")
models_h14, _, _ = train_svr_kfold(
    "h14/h2",
    {"kernel": "rbf", "C": 10, "epsilon": 0.00001, "gamma": 9.5},
    "models_svr/models_h14",
)

print("All models saved to models_svr/")
