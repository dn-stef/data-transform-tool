import numpy as np
import pandas as pd

def min_max_scale(dataset):
    min_val = dataset.min()
    max_val = dataset.max()
    if min_val == max_val:
        raise ValueError("Cannot min-max scale: all values are identical.")
    min_max_data = (dataset - min_val) / (max_val - min_val)
    return min_max_data

def standardization(dataset):
    mean = dataset.mean()
    std = dataset.std()
    if std == 0:
        raise ValueError("Cannot standardize: all values are identical.")
    standardized_data = (dataset - mean) / std
    return standardized_data

def log_transform(dataset):
    if (dataset <= 0).any():
        raise ValueError("Cannot log transform: all values must be positive.")
    log_data = np.log(dataset)
    return log_data

def square_root_transform(dataset):
    if (dataset < 0).any():
        raise ValueError("Cannot square root transform: all values must be non-negative.")
    sqrt_data = np.sqrt(dataset)
    return sqrt_data

def inverse_transform(dataset):
    if (dataset == 0).any():
        raise ValueError("Cannot inverse transform: dataset contains zero values.")
    inverse_data = 1 / dataset
    return inverse_data

def exponential_transform(dataset):
    if (dataset > 700).any():
        raise ValueError("Cannot exponential transform: values too large (would overflow).")
    exp_data = np.exp(dataset)
    return exp_data