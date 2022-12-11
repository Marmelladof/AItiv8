import sys
import os
import pickle

cwd = os.getcwd()
sys.path.insert(0, cwd + "/ml_section/model_training/")

# there are dependencies in model_traning for the unpickling
# however, not necessary to run model_training/main() to run model_testing/main()
# maybe it will receive parameters for optimization...
import model_training as mt

def main():
    with open("./ml_section/resources/trained_models/model1.sav", "rb") as file:
        model1 = pickle.load(file)
    
    print(model1.info)
    print(model1.get_testing_data())
    print(model1.model.get_degree([26,122,222,22.44516988,93.73763514,6.617227184,117.1843273]))
    
    # begin testing models here


# just for testing
# remove this line when model_testing is finished
# add it on __main__.py on model_run
main()