import json
import pickle

import numpy as np

import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

import pre_processing as pp
import utils
import elipsoide_model as epm

class Model1():
    # dedicated to the elipsoide model
    def __init__(self, n_init, X_train, X_test, y_train, y_test):
        self.info = {
            "model": "elipsoide model",
            "n_classes": 22
            }
        self.model = epm.ElipsoideModel(n_init=n_init)
        self.model.fit(X_train,y_train)

        self.training_data = {"X": X_train, "y": y_train}
        self.testing_data = {"X": X_test, "y": y_test}
    
    def get_training_data(self):
        return self.training_data
    
    def get_testing_data(self):
        return self.testing_data

class Model2():
    # similar to the above but to a neural network
    pass

# (...)

def main():
    # read dataset
    df = pd.read_csv("./ml_section/resources/Crop_recommendation.csv")

    status = pp.check_dataset(df)

    outliers_dict = pp.outlier_detection(df)
    
    # separation of independent and dependent variable and label encoding
    X = df.drop("label", axis=1)
    y = df["label"]
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    labels_dict = utils.dictify_labels(le.inverse_transform(y_encoded), y_encoded)
    with open("./ml_section/resources/encoded_labels.json", "w") as outputfile:
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

    # divide data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=500)

    # training elipsoide model and saving trained model
    n_init = 10
    model1 = Model1(n_init, X_train, X_test, y_train, y_test)
    with open("./ml_section/resources/trained_models/model1.sav", "wb") as file:
        pickle.dump(model1, file)

    # training NN model and saving trained model
    
    # training RF model and saving trained model

    # training N-B model and saving trained model