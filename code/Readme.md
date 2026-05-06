### Code Section

## Gradient_descent_algo.ipynb → `gradient_descent_demo/`

A minimal proof-of-concept neural network trained on synthetic data. It serves as the foundation for the gradient descent approach: the model's output is used as a loss function, and gradient descent is performed with respect to the *input features* (not model weights). This validates the idea of optimizing shape parameters via a surrogate model.

Converted to: [`01_train_simple_nn.py`](gradient_descent_demo/01_train_simple_nn.py), [`02_gradient_descent_features.py`](gradient_descent_demo/02_gradient_descent_features.py)

## Full_algo.ipynb → `full_algo/`

The complete data processing and analysis pipeline:

1. Load and merge `shape.csv` + `gradients.csv`
2. Compute normalized harmonic ratios h6/h2, h10/h2, h14/h2
3. Visualize raw heatmaps of harmonics over the (R, L) parameter space
4. Find the brute-force optimum on the 32×32 simulation grid
5. Train SVR models (10-fold cross-validation, R² > 0.987)
6. Smooth the 32×32 maps to 500×500 using trained SVR models
7. Gradient descent on shape parameters using the SVR ensemble as a loss
8. Visualization plots for the final presentation

Converted to: [`01_data_loading.py`](full_algo/01_data_loading.py) through [`08_visualization.py`](full_algo/08_visualization.py)
