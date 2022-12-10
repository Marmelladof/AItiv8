import os
import json

import numpy as np
import matplotlib.pyplot as plt

import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

import pre_processing as pp
import utils
import elipsoide_model as epm

def main():
    # read dataset
    os.chdir("ml_section")
    df = pd.read_csv("./resources/Crop_recommendation.csv")

    status = pp.check_dataset(df)

    outliers_dict = pp.outlier_detection(df)
    
    # separation of independent and dependent variable and label encoding
    X = df.drop("label", axis=1)
    y = df["label"]
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    labels_dict = utils.dictify_labels(le.inverse_transform(y_encoded), y_encoded)
    with open("./results/encoded_labels.json", "w") as outputfile:
        json.dump(labels_dict, outputfile)

    # converting back into a dataframe
    y_encoded = pd.DataFrame(y_encoded, columns=["label"])

    # adding interactions and selecting most important features
    X_inter = pp.add_interactions(X)
    selector = SelectKBest(chi2, k=len(df.columns.values)-1)
    X_inter_reduced = selector.fit_transform(X_inter,y)
    selected_features = X_inter.columns.values[selector.get_support()]
    # converting back into a dataframe
    X_inter_reduced = pd.DataFrame(X_inter_reduced, columns=selected_features)

    model1 = epm.ElipsoideModel(n_init=10)
    model1.fit(X,y_encoded)
    alligiance = model1.get_degree([56,58,49,37.13165026,94.60761797,6.69215564,172.47880619999995])
    with open("./results/elipsoide_method_alligiance.json", "w") as outputfile:
        json.dump(alligiance, outputfile)

if __name__ == "__main__":
    main()