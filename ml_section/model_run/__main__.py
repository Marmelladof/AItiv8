import pickle
import os
import sys

cwd = os.getcwd()
sys.path.insert(0, cwd + "/ml_section/model_training/")

# there are dependencies in model_traning for the unpickling
# however, not necessary to run model_training/main() to run model_testing/main()
# maybe it will receive parameters for optimization...
import model_training as mt

def run_model1(point):
    with open("./ml_section/resources/trained_models/model1.sav", "rb") as file:
        model1 = pickle.load(file)
    
    testing_data = model1.get_testing_data()
    X_test = testing_data["X"]
    y_test = testing_data["y"]
    
    alligiance = model1.model.get_degree(point)

    return alligiance

def main():
    # check if there are models serialized before runnning a new one
    # (run model_training ONCE)
    # run model_testing
    point = [90,46,42,23.97898217,81.45061596,7.50283396,250.0832336]
    alligiance1 = run_model1(point)
    print(alligiance1)

if __name__ == "__main__":
    main()