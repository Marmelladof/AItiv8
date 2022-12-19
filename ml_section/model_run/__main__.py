import pickle
import os
import sys

cwd = os.getcwd()
sys.path.insert(0, cwd + "/ml_section/model_training/")
sys.path.insert(0, cwd + "/ml_section/model_testing/")

# there are dependencies in model_traning for the unpickling
# however, not necessary to run model_training/main() to run model_testing/main()
# maybe it will receive parameters for optimization...
import model_training as mtr
import model_testing as mtt

def refresh_models():
    prompt_main = input("Do you wish to refresh the models? (y/n): ")
    if prompt_main == "y":
        prompt_sec = input("Do you wish to test the refreshed model? (y/n): ")
        if prompt_sec == "y":
            prompt_split = float(input("Test split size: "))
            prompt_rndstate = int(input("Define random state: "))
            # trains new model and serializes it
            mtr.main(prompt_split, prompt_rndstate)
            # tests the serialized model
            model_data = mtt.main()
            return model_data
        else:
            prompt_split = float(input("Test split size: "))
            prompt_rndstate = int(input("Define random state: "))
            mtr.main(prompt_split, prompt_rndstate)
            # trains new model and serializes it
            return None
    else:
        return None

def run_model1(point):
    # opens available serialized model 1
    with open("./ml_section/resources/trained_models/model1.sav", "rb") as file:
        model1 = pickle.load(file)
    
    alligiance = model1.model.get_degree(point)

    return alligiance

def main(point):
    # this function needs to be incoporated in the UI
    status = refresh_models()
    print(status)

    alligiance1 = run_model1(list(point.values()))
    print(alligiance1)

    return alligiance1

if __name__ == "__main__":
    point = {"N" : 90,
             "P" : 46,
             "K": 42,
             "temperature" : 23.97898217,
             "humidity" : 81.45061596,
             "ph" : 7.50283396,
             "rainfall" : 250.0832336}
    alligiance1 = main(point)