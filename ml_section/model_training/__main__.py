import os

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

import pre_processing as pp

def main():
    # read dataset
    os.chdir("ml_section")
    df = pd.read_csv("./resources/Crop_recommendation.csv")

    status = pp.check_dataset(df)
    print(status)

    outliers_dict = pp.outlier_detection(df)
    print(outliers_dict)
    
    # separation of independent and dependent variable and label encoding
    X = df.drop("label", axis=1)
    y = df["label"]
    le = LabelEncoder()
    y = le.fit_transform(y)

    # adding interactions and selecting most important features
    X_inter = pp.add_interactions(X)
    selector = SelectKBest(chi2, k=len(df.columns.values)-1)
    X_inter_reduced = selector.fit_transform(X_inter,y)
    print(f"Selected Features: {X_inter.columns.values[selector.get_support()]}")

if __name__ == "__main__":
    main()