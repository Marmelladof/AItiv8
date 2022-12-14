import sys
import os
import pickle

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix as conf_matrix
from sklearn.metrics import accuracy_score
import seaborn as sns

cwd = os.getcwd()
sys.path.insert(0, cwd + "/ml_section/model_training/")

# there are dependencies in model_traning for the unpickling
# however, not necessary to run model_training/main() to run model_testing/main()
# maybe it will receive parameters for optimization...
import model_training as mtr

def test_model1(model1):
    n_classes = model1.info["n_classes"]
    testing_data = model1.get_testing_data()

    X_test = testing_data["X"]
    y_test = testing_data["y"]

    validation = []
    conf_matrix = np.zeros([n_classes, n_classes])
    count = 0
    tolerance_update = 10
    model1.model.elipsoide_tol = tolerance_update
    n_positives = []
    for ipoint in range(X_test.shape[0]):
        point = np.array(X_test.iloc[ipoint])
        alligiance = model1.model.get_degree(point)
        items = list(alligiance.items())
        values = list(alligiance.values())
        highest_class = items[values.index(max(values))][0]
        correct_value = str(y_test.iloc[ipoint][0])
        if highest_class == correct_value:            
            validation.append(True)
            n_positives.append(sum([val > 0 for val in values]))
        else:
            validation.append(False)

        conf_matrix[int(correct_value), int(highest_class)] += 1

    conf_matrix = conf_matrix.astype(int)
    #print(f"List of n positives counts for tolerance of {model1.model.elipsoide_tol}: {n_positives}")

    return validation, conf_matrix

def test_model2(model2):
    n_classes = model2.info["n_classes"]
    testing_data = model2.get_testing_data()
    
    X_test = testing_data["X"]
    y_test = testing_data["y"]

    pred = model2.model.predict(X_test)
    
    return accuracy_score(pred, y_test), conf_matrix(y_test, pred)

def test_model3(model3):
    n_classes = model3.info["n_classes"]
    testing_data = model3.get_testing_data()

    X_test = testing_data["X"]
    y_test = testing_data["y"]

    pred = model3.model.predict(X_test)
    
    return accuracy_score(pred, y_test), conf_matrix(y_test, pred)
    
def main():
    # it only tests the available serialized models on resources/trained_models
    with open("./ml_section/resources/trained_models/model1.sav", "rb") as file:
        model1 = pickle.load(file)
    
    with open("./ml_section/resources/trained_models/model2.sav", "rb") as file1:
        model2 = pickle.load(file1)
    
    with open("./ml_section/resources/trained_models/model3.sav", "rb") as file2:
        model3 = pickle.load(file2)
    
    # begin testing models here
    # elipsoide model
    validation, conf_matrix = test_model1(model1)
    sucssess_rate = sum(validation)/len(validation)

    fig = plt.figure(figsize=(8, 8))
    sns.heatmap(conf_matrix, annot=True)
    plt.xlabel('Predictions', fontsize=18)
    plt.ylabel('Actuals', fontsize=18)
    plt.title('Confusion Matrix', fontsize=18)
    fig.savefig("./ml_section/images/confusion_matrix_model1.png")

    # NN model
    accuracy_score, conf_matrix = test_model2(model2)
    fig1 = plt.figure(figsize=(8,8))
    sns.heatmap(conf_matrix, annot=True)
    plt.xlabel("Predictions")
    plt.ylabel("Actuals")
    plt.title('Confusion Matrix', fontsize=18)
    fig1.savefig("./ml_section/images/confusion_matrix_model2.png")
    
    # Naive Bayes Model
    accuracy_score2, conf_matrix2 = test_model3(model3)
    fig2 = plt.figure(figsize=(8,8))
    sns.heatmap(conf_matrix2, annot=True)
    plt.xlabel("Predictions")
    plt.ylabel("Actuals")
    plt.title('Confusion Matrix', fontsize=18)
    fig2.savefig("./ml_section/images/confusion_matrix_model3.png")
    
    model_data = {model1.info["model"]: sucssess_rate}
    model_data1 = {model2.info["model"]: accuracy_score}
    model_data2 = {model3.info["model"]: accuracy_score2}
    return model_data, model_data1,model_data2