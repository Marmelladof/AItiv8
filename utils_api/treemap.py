import matplotlib.pyplot as plt
import squarify
import json


def plot_treemap(prediction, areas, tags):

    counter = 0
    for soil in prediction:
        key_list = list(soil)
        tracker = 0
        for key in key_list:
            if soil[key] >= 0:
                tracker += 1
                tags[counter] += "\n- {};".format(key)
        if tracker == 0:
            soil_values = list(soil.values())
            max_value = max(soil_values)
            value = (i for i in soil if soil[i]==max_value)
            tags[counter] += "\n(least worst idea)\n- {};".format(value)
        counter += 1

    squarify.plot(sizes=areas, label=tags, alpha=0.6 )
    plt.title('Land distribution as Crop suggestions')
    plt.xlabel('meters')
    plt.ylabel('meters')
    plt.savefig("delete.png")

    # TODO: Try to figure out how to send image array in Django
    # fig = plt.figure()
    # fig.canvas.draw()

    # # Now we can save it to a numpy array.
    # data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    # data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    # response = base64.b64encode(data)

    return