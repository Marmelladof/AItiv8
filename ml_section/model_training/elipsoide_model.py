from sklearn.cluster import KMeans

import pandas as pd

class ElipsoideModel():
    def __init__(self):
        self.elipsoide_params = {}
    
    def fit(self, X, y):
        classes = pd.unique(y["label"])
        cluster_centers = []
        classes_order = []
        for c in classes:
            kmeanModel = KMeans(n_clusters=1, n_init=10).fit(X.loc[y['label'] == c])
            centroids = kmeanModel.cluster_centers_
            cluster_centers.append(centroids)
            classes_order.append(c)
        
        i = 0
        for c in classes_order: 
            centroid = cluster_centers[i][0]
            class_cluster = X.loc[y['label'] == c]
            features = class_cluster.columns.values
            semiaxis = []
            j = 0
            for feature in features:
                semiaxis.append(class_cluster[feature].max() - centroid[j])
                j += 1
            
            i += 1
            
            self.elipsoide_params[str(c)] = {"center": centroid, "semiaxis": semiaxis}
        

    def get_degree(self, point):
        pass
        #sum = 0
        #for i in range(len(semiaxis)):
        #    sum += ((point[i] - centroid[i])**2)/((semiaxis[i])**2)