import sys
import os
import pickle

import numpy as np
import matplotlib.pyplot as plt

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
    confusion_matrix = np.zeros([n_classes, n_classes])
    for ipoint in range(X_test.shape[0]):
        point = np.array(X_test.iloc[ipoint])
        alligiance = model1.model.get_degree(point)

        items = list(alligiance.items())
        values = list(alligiance.values())
        highest_class = items[values.index(max(values))][0]
        correct_value = str(y_test.iloc[ipoint][0])
        if highest_class == correct_value:            
            validation.append(True)
        else:
            validation.append(False)

        confusion_matrix[int(correct_value), int(highest_class)] += 1

    return validation, confusion_matrix

def main():
    # it only tests the available serialized models on resources/trained_models
    with open("./ml_section/resources/trained_models/model1.sav", "rb") as file:
        model1 = pickle.load(file)
    
    # begin testing models here
    # elipsoide model
    validation, conf_matrix = test_model1(model1)
    conf_matrix = conf_matrix.astype(int)
    sucssess_rate = sum(validation)/len(validation)

    fig, ax = plt.subplots(figsize=(7.5, 7.5))
    ax.matshow(conf_matrix, cmap=plt.cm.Blues, alpha=0.3)
    for i in range(conf_matrix.shape[0]):
        for j in range(conf_matrix.shape[1]):
            ax.text(x=j, y=i,s=conf_matrix[i, j], va='center', ha='center', size='small')

    plt.xlabel('Predictions', fontsize=18)
    plt.ylabel('Actuals', fontsize=18)
    plt.title('Confusion Matrix', fontsize=18)
    fig.savefig("./ml_section/images/confusion_matrix_model1.png")

    # NN
    # (...)

    model_data = {model1.info["model"]: sucssess_rate}

    return model_data