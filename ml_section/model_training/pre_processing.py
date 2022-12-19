import os
import numpy as np
import matplotlib.pyplot as plt

import pandas as pd

from itertools import combinations
from sklearn.preprocessing import PolynomialFeatures


def check_dataset(df):
    # search for all classification data
    classes = pd.unique(df["label"])

    # checking if data is balanced
    last_dim = float("inf")
    lowest_dim = 0
    dimensions = []

    for lb in classes:
        class_dim = df.loc[df["label"] == lb, "label"].shape[0]
        dimensions.append(class_dim)
        if class_dim < last_dim:
            lowest_dim = class_dim
        
        last_dim = class_dim

    deviations = 100*(np.abs(np.array(dimensions) - lowest_dim)/lowest_dim)
    balance_tol = 10
    if all(deviations <= balance_tol):
        data_balanced = True
    else:
        data_balanced = False
    
    # Checking data quality
    if any(df.isna().sum() > 0):
        exists_nan = True
    else:
        exists_nan = False

    # Checking quantity of data points
    quantity_crit = 90
    if lowest_dim < quantity_crit:
        data_quantity = False
    else:
        data_quantity = True
    

    status = {
        "data_balancing":data_balanced, 
        "exists_nan": exists_nan, 
        "data_quantity": data_quantity}

    return status

def outlier_detection(df):
    # tukey method

    classes = pd.unique(df["label"]) 
    features = df.columns.values[:-1]

    outliers_dict = {}
    for c in classes:
        class_data = df.loc[(df["label"] == c)]
        for f in features:
            feature_data = class_data[f]
            q1 = np.percentile(feature_data, 25)
            q3 = np.percentile(feature_data, 75)
            iqr = q3-q1 
            floor = q1 - 1.5*iqr
            ceiling = q3 + 1.5*iqr
            outlier_indices = list(
                feature_data.index[(feature_data < floor)|(feature_data > ceiling)])
            outlier_values = list(
                feature_data[outlier_indices])

            outliers_dict[c + "_" + f] = (outlier_values, outlier_indices)

    return outliers_dict

def add_interactions(df):
    # Get feature names
    combos = list(combinations(list(df.columns), 2))
    colnames = list(df.columns) + ['_'.join(x) for x in combos]
    
    # Find interactions
    poly = PolynomialFeatures(interaction_only=True, include_bias=False)
    df = poly.fit_transform(df)
    df = pd.DataFrame(df)
    df.columns = colnames
    
    # Remove interaction terms with all 0 values            
    noint_indicies = [i for i, x in enumerate(list((df == 0).all())) if x]
    df = df.drop(df.columns[noint_indicies], axis=1)
    
    return df