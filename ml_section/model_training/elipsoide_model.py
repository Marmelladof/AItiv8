
class ElipsoideModel():
    cluster_centers = []
    K = range(1,10)
    for k in numeric_list:
        kmeanModel = KMeans(n_clusters=1).fit(df.loc[df['label'] == k])
        kmeanModel.fit(df.loc[df['label'] == k])
        centroids = kmeanModel.cluster_centers_
        cluster_centers.append(centroids)
    
    centroid = cluster_centers[0][0]
    rice_cluster = df.loc[df['label'] == 0]
    features = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    max_features = []
    for feature in features:
        max_features.append(rice_cluster[feature].max())

    ponto_aleatorio_arroz = [85, 58, 41, 21.770462, 80.319644, 7.038096, 226.655537]
    ponto_aleatorio_milho = [107, 34, 32, 26.774637, 66.413269, 6.780064, 177.774507]
    sum = 0
    for i in range(len(max_features)):
        sum += ((ponto_aleatorio_milho[i] - centroid[i])**2)/((max_features[i])**2)