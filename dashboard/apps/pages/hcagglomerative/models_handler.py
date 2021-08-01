
from sklearn.cluster import KMeans, AgglomerativeClustering

class ModelHandler():
    def __init__(self):
        pass
    
    def get_clusters(self, request_data, enconded_data):

        hc = AgglomerativeClustering(n_clusters=int(request_data["nClusters"]), linkage=request_data["linkage"])
        y = hc.fit(enconded_data.toarray()).labels_

        return y