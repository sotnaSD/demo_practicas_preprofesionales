
from sklearn.cluster import KMeans, AgglomerativeClustering

class ModelHandler():
    def __init__(self):
        pass
    
    def get_clusters(self, request_data, enconded_data):
        km = KMeans(n_clusters=int(request_data["nClusters"]), random_state=1000)  # It uses by default KMeans ++
        y = km.fit_predict(enconded_data)
        return y
    