import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import squarify
import numpy as np

def plot_treemap(prediction, areas, tags):

    counter = 0
    print(tags)
    for soil in prediction:
        del soil["area"]
        key_list = list(soil)
        tracker = 0
        for key in key_list:
            if key == "area":
                continue
            elif soil[key] >= 0:
                tracker += 1
                tags[counter] = "{}\n- {};".format(str(tags[counter]), str(key))
        if tracker == 0:
            soil_values = list(soil.values())
            max_value = max(soil_values)
            value = ([i for i in soil if soil[i]==max_value])
            tags[counter] = "{}\n(least worst idea)\n- {};".format(str(tags[counter]), str(value[0]))
        counter += 1

    squarify.plot(sizes=areas, label=tags, alpha=0.6 )
    plt.title('Land distribution as Crop suggestions')
    plt.xlabel('meters')
    plt.ylabel('meters')
    plt.savefig("delete.png")
    plt.clf()

    return

def plot_final_treemap(prediction, areas):

    counter = 0
    tags = []
    area_list = []
    key_list = list(prediction.keys())
    counter = 0
    for key in key_list:
        counter += 1
        area = areas[key]
        for crop in prediction[key]:
            area_list.append(int(area/len(prediction[key])))
            tags.append(f"area{counter}\n{crop}")
    print(area_list)
    print(tags)
    squarify.plot(sizes=area_list, label=tags, alpha=0.6 )
    plt.title('Land distribution as Crop suggestions')
    plt.xlabel('meters')
    plt.ylabel('meters')
    plt.savefig("final.png")
    plt.clf()

    return

def plot_cvp_bar_chart(selected_crops, prod, consumptions):
    X = selected_crops
    Yproduction = prod
    Zconsumption = consumptions

    X_axis = np.arange(len(X))
    plt.figure(figsize=(10, 5))  # width:20, height:3
    plt.bar(X_axis - 0.2, Yproduction, align='center', width=0.4, label = 'Production')
    plt.bar(X_axis + 0.2, Zconsumption, align='center', width=0.4, label = 'Consumption')
    
    plt.xticks(X_axis, X)
    plt.xlabel("Crops")
    plt.ylabel("Kg of crops")
    plt.title("Consumption and Production comparison")
    plt.legend()
    plt.savefig("cons_prod.png")
    plt.clf()

def plot_money_bar_chart(selected_crops, guito_per_crop):
    X = selected_crops
    Ymoney = guito_per_crop

    X_axis = np.arange(len(X))
    print(X)
    print(Ymoney)
    
    plt.figure(figsize=(10, 5))  # width:20, height:3
    plt.bar(X_axis, Ymoney, align='center', width=0.4)
    
    plt.xticks(X_axis, X)
    plt.xlabel("Crops")
    plt.ylabel("Euros")
    plt.title("Gross income per crop")
    plt.legend()
    plt.savefig("money.png")
    plt.clf()