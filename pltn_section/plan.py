import os
import sys
import json

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

        return self.cleaned_soils, self.selected_items


def prepare(interests, consumptions, soils, areas):
    # assuming all arguments are dictionaries!
    colector = Collector()
    for soil in soils:
        point = list(soils[soil].values())
        model1_degree, model2_degree, model3_degree = run_model.main(point)
        colector.deposit_soil(model1_degree, 0)
    
    cleaned_soils, selected_crops = colector.unpack_soils()

    print(f"Model 1 recomendations for each given soil: {cleaned_soils}.")

    tot = 0
    for a in areas:
        tot += areas[a]
    for a in areas:
        areas[a] = areas[a]/tot

    print(areas)

    tot = 0
    relevant_consumptions = {}
    for s in selected_crops:
        tot += consumptions[s]
    for s in selected_crops:
        relevant_consumptions[s] = consumptions[s]/tot

    print(relevant_consumptions)

    diversity = 1/len(relevant_consumptions)

    print(diversity)

    with open("./pltn_section/resources/prices.json", "r") as file:
        prices = json.load(file)
    
    tot = 0
    relevant_prices_norm = {}
    relevant_prices = {}
    for s in selected_crops:
        relevant_prices[s] = prices[s]
        tot += prices[s]
    for s in selected_crops:
        relevant_prices_norm[s] = prices[s]/tot

    print(relevant_prices)
    print(relevant_prices_norm)

    crop_ponderation = dict()
    for s in selected_crops:
        crop_ponderation[s] = sum(
            [
                interests["sustainability"]*relevant_consumptions[s],
                interests["variety"]*diversity,
                interests["export"]*relevant_prices_norm[s]
            ]
        )

    print(crop_ponderation)

    with open("./pltn_section/resources/yield.json", "r") as file:
        crop_yields = json.load(file)

    tot = 0
    crop_yield_norm = {}
    crop_yield = {}
    for s in selected_crops:
        crop_yield[s] = crop_yields[s]
        tot += crop_yields[s]
    for s in selected_crops:
        crop_yield_norm[s] = crop_yields[s]/tot

    print(crop_yield)
    print(crop_yield_norm)

    for s in selected_crops:
        crop_ponderation[s] = crop_ponderation[s]*crop_yield_norm[s]
    
    tot = 0
    for c in crop_ponderation:
        tot += crop_ponderation[c]
    for c in crop_ponderation:
        crop_ponderation[c] = crop_ponderation[c]/tot

    print(crop_ponderation)

    return cleaned_soils, crop_ponderation

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

    consumptions = {
        "0": 18,
        "1": 12,
        "2": 87,
        "3": 98,
        "4": 34,
        "5": 45,
        "6": 10,
        "7": 68,
        "8": 88,
        "9": 22,
        "10": 345,
        "11": 290,
        "12": 3,
        "13": 7,
        "14": 31,
        "15": 42,
        "16": 56,
        "17": 23,
        "18": 238,
        "19": 439,
        "20": 25,
        "21": 4,
    }

    interests = {
        "sustainability": 0.4,
        "variety": 0.4,
        "export": 0.2
    }

    prepare(interests, consumptions, soils, areas)

main()