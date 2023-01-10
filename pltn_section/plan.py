import os
import sys
import json
import random
import copy

import numpy as np
import math

cwd = os.getcwd()
sys.path.insert(0, cwd + "/ml_section/model_run/")

import run_model

class Collector():
    def __init__(self) -> None:
        self.selected_items = []
        self.cleaned_soils = dict()
        self.n_soils = 0

    def deposit_soil(self, prediction, inclusion):
        cleaned_soil = {}
        sugestion = False
        for item in prediction:
            if prediction[item] > inclusion:
                sugestion = True
                cleaned_soil[item] = prediction[item]
                self.selected_items.append(item)
        
        if not sugestion:
            print("All negative! No good solution.")
            values = list(prediction.values())
            keys = list(prediction.keys())
            least_worst_index = values.index(max(values))
            least_worst_key = keys[least_worst_index]
            cleaned_soil[least_worst_key] = prediction[least_worst_key]
            self.selected_items.append(least_worst_key)

        self.n_soils += 1
        self.cleaned_soils["soil" + str(self.n_soils)] = cleaned_soil

        return self.cleaned_soils

    def unpack_soils(self):
        for cs in self.cleaned_soils:
            for st in self.selected_items:
                if not st in self.cleaned_soils[cs]:
                    self.cleaned_soils[cs][st] = 0

        #for cs in self.cleaned_soils:
        #    for st in self.selected_items:
        #        self.cleaned_soils[cs][st] = self.cleaned_soils[cs][st]

        # conversion to labels
        #with open("./ml_section/resources/encoded_labels.json") as file:
        #    encoded_labels = json.load(file)

        #decoded_labels = {}
        #decoded_items = []
        #for soil in self.cleaned_soils:
        #    decoded_labels[soil] = {}
        #    for label in encoded_labels:
        #        if str(encoded_labels[label]) in self.cleaned_soils[soil]:
        #            decoded_labels[soil][label] = self.cleaned_soils[soil][str(encoded_labels[label])]
        #            decoded_items.append(label)
        

        return self.cleaned_soils, list(np.unique(self.selected_items))

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
        consumptions.append((random.random()*2 + 1)*population)

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
    # apply gaussian filter
    mu = 1 # value to bring up
    sigma = math.sqrt(mu) # to cut at 2 +/- mu
    gauss_filter = lambda x: (math.exp((-(x-mu)**2)/(2*sigma**2))/(sigma*math.sqrt(2*math.pi)))/(1/(sigma*math.sqrt(2*math.pi)))
    # value between 0 and 1
    return gauss_filter((np.sum(np.array(prod)/np.array(cons))/len(cons)))

def func_vary(prod, used_crops, total_crops):
    prod_norm = list(map(lambda x: x/sum(prod), prod))

    # gaussian filter
    mu = 1/len(prod) # value to bring up
    sigma = math.sqrt(0.05*mu) # to cut at 0.1 +/- mu
    gauss_filter = lambda x: (math.exp((-(x-mu)**2)/(2*sigma**2))/(sigma*math.sqrt(2*math.pi)))/(1/(sigma*math.sqrt(2*math.pi)))
    filtered_prod = list(map(gauss_filter, prod_norm))
    weight_prod = sum(filtered_prod)/len(filtered_prod)

    # used_crop/total_crop is between 0 and 1
    # weight_prod is between 0 and 1
    return weight_prod*used_crops/total_crops

def func_export(crop_relevance, crop_area):
    # crop_area is the calculated area that a crop covers
    # in a certain configuration

    # units €
    guito_per_crop = np.array(crop_relevance)*np.array(crop_area)
    
    # not sure tho...
    return np.sum(guito_per_crop)

def maximum_guito(cleaned_soils, selected_crops, crop_relevance, areas):
    config = {}
    max_guito = 0
    for soil in cleaned_soils:
        first_loop = True
        for crop in cleaned_soils[soil]:
            if first_loop:
                if cleaned_soils[soil][crop] != 0:
                    first_loop = False
                    # it is not the best yet, but it is the first non null.
                    # has the possibility of being the best
                    best_crop = crop
                    continue
                else:
                    continue

            else: 
                if cleaned_soils[soil][crop] != 0:
                    if crop_relevance[selected_crops.index(crop)] > crop_relevance[selected_crops.index(best_crop)]:
                        best_crop = crop
        
        max_guito += crop_relevance[selected_crops.index(best_crop)]*areas[soil]
        config[soil] = [best_crop]

    return max_guito, config

def func_quality(cleaned_soils, solution):
    adjustment = 0
    soils_adjustment = []
    for soil in solution:
        counts = 0
        for crop in solution[soil]:
            counts += 1
            adjustment += cleaned_soils[soil][crop]
        
        soils_adjustment.append(adjustment/counts)
    
    return sum(soils_adjustment)

def gen_population(domain, n_sols):
    population = []
    for i in range(n_sols):
        domain_copy = copy.deepcopy(domain)
        population.append({})
        for soil in domain_copy:
            population[i][soil] = []
            popped_crop = random.randint(0, len(domain_copy[soil])-1)
            population[i][soil].append(domain_copy[soil].pop(popped_crop))
            division_prob = random.randint(1, 2)
            while len(domain_copy[soil]) >= 1 and division_prob == 1 and len(population[i][soil]) <= 6:
                popped_crop = random.randint(0, len(domain_copy[soil])-1)
                population[i][soil].append(domain_copy[soil].pop(popped_crop))
                
                division_prob = random.randint(1, 2)

    return population

def crossover(population):
    population_copy = copy.deepcopy(population)
    for i in range(0, len(population)-1, 2):
        random_soil = random.choice(list(population_copy[i].keys()))
        # print(f"Swapped {random_soil} in between solutions {i} and {i+1}")
        swap1 = population_copy[i][random_soil]
        swap2 = population_copy[i+1][random_soil]
        population_copy[i][random_soil] = swap2
        population_copy[i+1][random_soil] = swap1

    population = population + population_copy

    return population

def mutation(population, domain):
    for i in range(len(population)):
        domain_copy = copy.deepcopy(domain)
        mutation_chance = random.randint(1, len(population))
        if mutation_chance == 1:
            random_soil = random.choice(list(population[i].keys()))
            # print(f"Mutation applied to solution {i} on {random_soil}")
            population[i][random_soil] = []
            popped_crop = random.randint(0, len(domain_copy[random_soil])-1)
            population[i][random_soil].append(domain_copy[random_soil].pop(popped_crop))
            division_prob = random.randint(1, 2)
            while len(domain_copy[random_soil]) >= 1 and division_prob == 1 and len(population[i][random_soil]) <= 5:
                popped_crop = random.randint(0, len(domain_copy[random_soil])-1)
                population[i][random_soil].append(domain_copy[random_soil].pop(popped_crop))
                
                division_prob = random.randint(1, 2)
    
    return population

def optimization(predictions, areas, population, interests):
    # solution structure example:
    # {
    #   "soil1": ["rice"],
    #   "soil2": ["maize", "mothbeans"], ---> here there was a division!
    #   "soil3": ["banana"]
    # }
    # {
    #   "soil1": ["rice", "jute"],
    #   "soil2": ["maize"],
    #   "soil3": ["banana"]
    # }
    #
    # Cross-overs: swap respective soils at random;
    # Mutation: select another available crop at random for on random soil;
    cleaned_soils, selected_crops, consumptions, total_crops, crop_relevance = prepare(population, predictions)
    
    with open("./pltn_section/resources/yield.json", "r") as file:
        crop_yields = json.load(file)

    max_guito, config = maximum_guito(cleaned_soils, selected_crops, crop_relevance, areas)
    domain = {}
    for soil in cleaned_soils:
        domain[soil] = []
        for crop in cleaned_soils[soil]:
            if cleaned_soils[soil][crop] != 0:
                domain[soil].append(crop)

    # generate initial population
    n_sols = 6
    population = gen_population(domain, n_sols)

    iterations = 0
    max_iterations = 150
    while iterations <= max_iterations:
        #print("-------------------------")
        #print(f"Generation: {iterations}")

        # generate offspring (cross-over)
        population = crossover(population)

        # mutations
        population = mutation(population, domain)

        # calculating objective function
        total_func = []
        for solution in population:
            prod = [0 for i in range(len(selected_crops))]
            used_crops = []
            crop_area = [0 for i in range(len(selected_crops))]
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
            variety = func_vary(prod, used_crops, total_crops)
            # export objective function
            export = func_export(crop_relevance ,crop_area)/max_guito
            # soil quality
            soils_adjustment = func_quality(cleaned_soils, solution)

            total_func.append(soils_adjustment*(interests["sustainability"]*sustainability + interests["variety"]*variety + interests["export"]*export))

        # selection
        offspring = []
        offspring_vals = []
        # chosing the best and worst randomly out of the total population
        for i in range(n_sols):
            prob_max_min = random.randint(1, 100)
            # 80% probability of choosing a maximum
            if prob_max_min <= 80:
                #print("Fetched a fit solution")
                max_id_sol = total_func.index(max(total_func))
                offspring_vals.append(total_func.pop(max_id_sol))
                offspring.append(population[max_id_sol])

            # 20% probability of choosing a minimum
            else:
                #print("Fetched a non-fit solution")
                min_id_sol = total_func.index(min(total_func))
                offspring_vals.append(total_func.pop(min_id_sol))
                offspring.append(population[min_id_sol])

        # new population
        total_func = []
        population = []
        population = population + offspring

        iterations += 1
    
    solution_val = max(offspring_vals)
    solution = offspring[offspring_vals.index(solution_val)]
    prod = [0 for i in range(len(selected_crops))]
    used_crops = []
    crop_area = [0 for i in range(len(selected_crops))]
    divisions_list = []
    for soil in solution:
        divisions = len(solution[soil])
        divisions_list.append(divisions)
        area_of_soil = areas[soil]
        for crop in solution[soil]:
            prod[selected_crops.index(crop)] += crop_yields[crop]*area_of_soil/divisions
            crop_area[selected_crops.index(crop)] += area_of_soil/divisions
            used_crops.append(crop)
        
    used_crops = list(np.unique(used_crops))

    guito_per_crop = list(np.array(crop_relevance)*np.array(crop_area))

    return solution, solution_val, selected_crops, used_crops, prod, consumptions, guito_per_crop

def main():
    #soils = {"soil1": 
    #            # rice
    #            {"N" : 59,
    #             "P" : 48,
    #             "K": 39,
    #             "temperature" : 24.28209415,
    #             "humidity" : 80.30025587,
    #             "ph" : 7.1422990689999985,
    #             "rainfall" : 231.0863347},
    #         "soil2":
    #            # maize
    #            {"N" : 64,
    #             "P" : 35,
    #             "K": 23,
    #             "temperature" : 23.02038334,
    #             "humidity" : 61.89472002,
    #             "ph" : 5.680361037999999,
    #             "rainfall" : 63.03843397},
    #         "soil3":
    #            # banana
    #            {"N" : 95,
    #             "P" : 74,
    #             "K": 50,
    #             "temperature" : 25.90113128,
    #             "humidity" : 80.47152737,
    #             "ph" : 6.002481605,
    #            "rainfall" : 110.10323}}

    areas = {
        "soil1": 200,
        "soil2": 330,
        "soil3": 90
    }

    population = 100

    interests = {
        "sustainability": 0.4,
        "variety": 0.4,
        "export": 0.2
    }

    #predictions = {}
    #for soil in soils:
    #    point = list(soils[soil].values())
    #    model1_degree, model2_degree, model3_degree = run_model.main(point)
    #    predictions[soil] = model1_degree
    predictions = {"16":{
        "apple":-62.43993815437476,
        "banana":-5.5980370257636825,
        "blackgram":-5.427152061740048,
        "chickpea":-1.3916505519489915,
        "coconut":-9.457737305835531,
        "coffee":-0.8187847632211338,
        "cotton":-5.675964695501701,
        "grapes":-77.09596943982712,
        "jute":-1.0305843749397874,
        "kidneybeans":-1.1621848976837554,
        "lentil":-5.696647248381201,
        "maize":-1.4934071983003647,
        "mango":-2.56755717383554,
        "mothbeans":-2.0135060633490816,
        "mungbean":-11.238418210807838,
        "muskmelon":-40.81081199518549,
        "orange":-29.945882694489228,
        "papaya":-29.452976518363347,
        "pigeonpeas":-1.3357605336000646,
        "pomegranate":-9.373243666901672,
        "rice":-20.475226283624988,
        "watermelon":-8.725627463813085
    }}
    data = optimization(predictions, areas, population, interests)
    print(data)

main()