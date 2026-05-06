<div align="center">

# Magnet Pole Shape Optimization

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&pause=1000&color=4F94EF&center=true&vCenter=true&width=700&lines=ML-driven+magnet+pole+optimization;SVR+regression+%2B+gradient+descent;Opera+3D+simulation+automation;1024+training+samples+collected" alt="Typing animation" />

[![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5.2-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![Opera 3D](https://img.shields.io/badge/Opera_3D-Simulation-6C3483?style=for-the-badge)](https://www.cobham.com/mission-systems/antenna-systems/by-product/opera/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## Overview

This project solves the **inverse problem** of magnet pole shape design: given a target field quality, find the geometry parameters that minimize parasitic harmonics.

The goal is to select an **optimal pole shape** that suppresses the **6th, 10th, and 14th harmonics** of the tangential magnetic field decomposed on a circle of radius **0.8 × aperture**, centered at the origin in the plane perpendicular to the beam axis.

The magnet has shape hyperparameters such as:
- `Shim center position`
- `Hyperbola breakpoint`
- `Hyperbola height`
- `Shim curvature radius`
- `...`

The example considered in this work uses a simpler pole geometry with **two parameters**:

<div align="center">
<img 
  src="https://github.com/Askash1234567890/Diplome/blob/main/pictures/рисунок_полюса.png"
  alt="Pole Geometry"
  width="500"
/>
</div>

Data collection macro schema and database structure:

<div align="center">
<img
  src="https://github.com/Askash1234567890/Diploma/blob/main/pictures/схема_алгоритма_сбора_данных.png"
  alt="Data Collection Scheme"
  width="900"
/>
</div>

---

## How It Works

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Generate 1024  │───▶│  Run Opera 3D   │───▶│  Collect field  │
│  shape configs  │    │  simulations    │    │  harmonics data │
└─────────────────┘    └─────────────────┘    └────────┬────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Gradient desc. │◀───│  Train SVR      │◀───│  Merge shape +  │
│  on features    │    │  models (KFold) │    │  harmonics data │
└────────┬────────┘    └─────────────────┘    └─────────────────┘
         │
         ▼
┌─────────────────┐
│  Optimal pole   │
│  shape params   │
└─────────────────┘
```

---

## Solution Pipeline

- [x] Learn how to build geometry in `Opera 3D`
- [x] Write a script that iterates over shape hyperparameters, computes **h6, h10, h14** field harmonics, and saves them to a database — collecting *training* data
- [x] Accumulate `1024` training examples
- [x] Train ML models to regress h6, h10, h14 harmonics from shape parameters
- [x] Apply **gradient descent** with shape parameters as optimization variables and fixed model weights (loss = sum of h6, h10, h14 predictions from the regression models)
- [x] Obtain the final optimal shape

## Future Work

- [ ] Build a unified `Opera` assembly for a complete API
- [ ] Try **genetic algorithms**
- [ ] Try **reinforcement learning**

---

## Scalability

> If this algorithm is implemented for a problem with *two* degrees of shape freedom, it scales naturally to more complex geometries where the optimal form is not obvious. This project demonstrates the approach on a simple example — parallelpiped pole pieces with chamfers.

---

## Project Structure

```
Diploma/
├── code/                          # Jupyter notebooks & Python scripts
│   ├── full_algo/                 # Full pipeline: data → models → optimization
│   │   ├── 01_data_loading.py
│   │   ├── 02_eda_heatmaps.py
│   │   ├── 03_brute_force_optimum.py
│   │   ├── 04_model_training.py
│   │   ├── 05_model_inference.py
│   │   ├── 06_surface_smoothing.py
│   │   ├── 07_gradient_descent.py
│   │   └── 08_visualization.py
│   └── gradient_descent_demo/     # Proof-of-concept: gradient descent on NN
│       ├── 01_train_simple_nn.py
│       └── 02_gradient_descent_features.py
├── data/                          # Simulation output CSVs
│   ├── shape.csv                  # Shape parameters (R, L) with IDs
│   └── gradients.csv              # Field harmonics h0–h14 with IDs
├── scripts/                       # Opera automation scripts
│   ├── scripts.py                 # Clean raw logs → .comi files
│   ├── make_scripts.py            # Generate 1024 .comi shape configs
│   ├── make_1_script.py           # Generate single test .comi file
│   ├── get_harmonics.py           # Extract harmonics from Opera output
│   └── helper.py                  # Shared paths and templates
├── macro/
│   └── clicker.py                 # Mouse/keyboard automation for Opera
├── logs/                          # Raw Opera command logs
├── pictures/                      # Diagrams and figures
├── trained_models_and_other_zip_files/  # Pre-trained SVR models
└── requirements.txt
```

---

## Results

The ML-guided gradient descent found a shape that achieves **~5.3% lower loss** than the brute-force optimum found by exhaustive search over the 1024 sampled configurations:

| Method | Loss (sum of normalized h6/h2 + h10/h2 + h14/h2) |
|---|---|
| Brute-force (32×32 grid) | 0.2763 |
| **ML gradient descent** | **0.2616** |

The SVR models achieved **R² > 0.987** on cross-validation (10 folds) for all three harmonics.

---

## Quickstart

```bash
pip install -r requirements.txt

# Generate simulation scripts
python scripts/make_scripts.py

# After running Opera and collecting data, run the full pipeline:
cd code/full_algo
python 01_data_loading.py
python 02_eda_heatmaps.py
python 03_brute_force_optimum.py
python 04_model_training.py
# ... or use pre-trained models from trained_models_and_other_zip_files/models_2.zip
python 05_model_inference.py
python 07_gradient_descent.py
```

---

<div align="center">

*Final Bachelor's Thesis — Physics & ML intersection*

</div>
