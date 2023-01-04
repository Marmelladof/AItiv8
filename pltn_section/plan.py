import os
import sys
import json
import random

import numpy as np
import math

cwd = os.getcwd()
sys.path.insert(0, cwd + "/ml_section/model_run/")

import run_model

class Collector():
    def __init__(self) -> None:
        self.selected_items = set()
        self.cleaned_soils = dict()
        self.n_soils = 0

    def deposit_soil(self, prediction, inclusion):
        cleaned_soil = {}
        for item in prediction:
            if prediction[item] > inclusion:
                cleaned_soil[item] = prediction[item]
                self.selected_items.add(item)
        
        self.n_soils += 1
        self.cleaned_soils["soil" + str(self.n_soils)] = cleaned_soil

        return self.cleaned_soils

    def unpack_soils(self):
        tot_dict = {}
        for cs in self.cleaned_soils:
            tot = 0
            for st in self.selected_items:
                if not st in self.cleaned_soils[cs]:
                    self.cleaned_soils[cs][st] = 0
            
                tot += self.cleaned_soils[cs][st]

            tot_dict[cs] = tot

        for cs in self.cleaned_soils:
            for st in self.selected_items:
                self.cleaned_soils[cs][st] = self.cleaned_soils[cs][st]/tot_dict[cs]

        # conversion to labels
        with open("./ml_section/resources/encoded_labels.json") as file:
            encoded_labels = json.load(file)

        decoded_labels = {}
        decoded_items = []
        for soil in self.cleaned_soils:
            decoded_labels[soil] = {}
            for label in encoded_labels:
                if str(encoded_labels[label]) in self.cleaned_soils[soil]:
                    decoded_labels[soil][label] = self.cleaned_soils[soil][str(encoded_labels[label])]
                    decoded_items.append(label)

        return decoded_labels, np.unique(decoded_items)

def prepare(population, predictions):
    # assuming all arguments are dictionaries!
    colector = Collector()
    for soil in predictions:
        # soils will contain calculated point by the model
        colector.deposit_soil(predictions[soil], 0)
    
    # soils with the poderations per crop and added zeros in missing categories
    # adimensional (percentage)
    cleaned_soils, selected_crops = colector.unpack_soils()

    print(f"Model 1 recomendations for each given soil: {cleaned_soils}.")
    print(selected_crops)

    # FROM NOW ON, LISTS ARE IN THE ORDER OF SELECTED_CROPS SET

    # Self-Sustainability section
    # map population to consumptions
    consumptions = []
    for s in selected_crops:
        consumptions.append((random.random()*3)*population)

    # diversity equation proportional to n selected crops
    # only enters in the main part of the search
    total_crops = len(selected_crops)

    # crop relevance in exportation
    with open("./pltn_section/resources/prices.json", "r") as file:
        prices = json.load(file)
    
    with open("./pltn_section/resources/yield.json", "r") as file:
        crop_yields = json.load(file)

    crop_relevance = []
    for s in selected_crops:
        # units €/m²
        crop_relevance.append(prices[s]*crop_yields[s])


    return cleaned_soils, selected_crops, consumptions, total_crops, crop_relevance

def func_sus(prod, cons):
    # when consumption = production -> returns 1
    # apply poisson filter
    # filter_func = lambda x: (math.exp(-0.9)*0.9**x)/math.factorial(x)
    filter_func = lambda x: x
    # value between 0 and 1
    return filter_func((np.sum(np.array(prod)/np.array(cons))/len(cons)))

def func_vary(used_crops, total_crops):
    # value between 0 and 1
    return used_crops/total_crops

def func_export(crop_relevance, crop_area):
    # crop_area is the calculated area that a crop covers
    # in a certain configuration

    # units €
    guito_per_crop = np.array(crop_relevance)*np.array(crop_area)
    
    # not sure tho...
    return np.sum(guito_per_crop)

def optimization(cleaned_soils, selected_crops, consumptions, total_crops, crop_relevance, areas, interests):
    # solution structure example:
    # {
    #   "soil1": ["rice"],
    #   "soil2": ["rice", "jute"] ---> here there was a division!
    #   "soil3": ["jute"]
    # }

    with open("./pltn_section/resources/prices.json", "r") as file:
        crop_prices = json.load(file)
    
    with open("./pltn_section/resources/yield.json", "r") as file:
        crop_yields = json.load(file)

    # hypothetical generated solution
    solution = {}

    prod = [0 for i in range(selected_crops)]
    used_crops = []
    crop_area = [0 for i in range(selected_crops)]
    divisions_list = []
    for soil in solution:
        divisions = len(solution[soil])
        divisions_list.append(divisions)
        area_of_soil = areas[soil]
        for crop in solution[soil]:
            prod[selected_crops.index(crop)] += crop_yields[crop]*area_of_soil/divisions
            crop_area[selected_crops.index(crop)] += area_of_soil/divisions
            used_crops.append(crop)

    used_crops = len(np.unique(used_crops))

    # sustainability objective function calculation
    sustainability = func_sus(prod, consumptions)
    # variety objective function calculation
    variety = func_vary(used_crops, len(selected_crops))
    # export objective function (DISCUSS RETURN OF THE EXPORT FUNCTION!!!!)
    export = func_export(crop_relevance ,crop_area)

    total_func = interests["sustainability"]*sustainability + interests["variety"]*variety + interests["export"]*export - sum(divisions)

def main():
    soils = {"soil1": 
                # rice
                {"N" : 59,
                 "P" : 48,
                 "K": 39,
                 "temperature" : 24.28209415,
                 "humidity" : 81.30025587,
                 "ph" : 7.1422990689999985,
                 "rainfall" : 231.0863347},
             "soil2":
                # maize
                {"N" : 64,
                 "P" : 35,
                 "K": 23,
                 "temperature" : 23.02038334,
                 "humidity" : 61.89472002,
                 "ph" : 5.680361037999999,
                 "rainfall" : 63.03843397},
             "soil3":
                # banana
                {"N" : 95,
                 "P" : 74,
                 "K": 50,
                 "temperature" : 25.90113128,
                 "humidity" : 80.47152737,
                 "ph" : 6.002481605,
                 "rainfall" : 110.10323}}

    areas = {
        "soil1": 200,
        "soil2": 330,
        "soil3": 50
    }

    population = 100

    interests = {
        "sustainability": 0.4,
        "variety": 0.4,
        "export": 0.2
    }

    predictions = {}
    for soil in soils:
        point = list(soils[soil].values())
        model1_degree, model2_degree, model3_degree = run_model.main(point)
        predictions[soil] = model1_degree

    cleaned_soils, selected_crops, consumptions, total_crops, crop_relevance = prepare(population, predictions)
    optimization(cleaned_soils, selected_crops, consumptions, total_crops, crop_relevance, areas, interests)

main()