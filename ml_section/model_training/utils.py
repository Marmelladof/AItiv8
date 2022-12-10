import numpy as np

def dictify_labels(non_coded, coded):
    non_coded_elm = np.unique(non_coded)
    coded_elm = np.unique(coded)

    labels_dict = {}
    for i in range(len(non_coded_elm)):
        labels_dict[non_coded_elm[i]] = coded_elm[i]

    return labels_dict