import numpy as np
from sklearn.cluster import KMeans

class Optimizer():
    def __init__(self):
        pass
    
    def get_data_structure(self, data_encoded, init=2, end=30, n_values=4):
        if data_encoded.shape[0] < end:
            end = data_encoded.shape[0] - 1

        print('  Finding optimum value for K...')
        inercias = np.zeros(shape=(end - init + 1,))
        for i in range(init, end + 1):
            km = KMeans(n_clusters=i, random_state=1000)  # It uses by default KMeans ++
            km.fit(data_encoded)
            inercias[i - init] = km.inertia_

        # get the differences between i and i - 1
        diff = [inercias[i - 1] - inercias[i] for i in range(1, len(inercias))]
        # I need the + 3 because KMeans stats at 2 clusters, and the [0] takes the main result
        best_n_clusters = [diff.index(x) + 3 for x in sorted(diff, reverse=True)][:n_values]
        
        response_data = self._parse_response_data(data_encoded.shape[0], diff, best_n_clusters, n_values)

        return response_data, best_n_clusters
    
    def _parse_response_data(self, n_docs, diff, best_n_clusters, n_values):
        resp_data = {}
        resp_data['n_docs'] = n_docs
        resp_data['var_dropdown'] = round(np.var(diff), 2)
        resp_data['avg_dropdown'] = round(sum(diff) / len(diff), 2)
        resp_data['best_n_clusters'] = []

        for i in range(n_values):
            resp_data['best_n_clusters'].append({'ranking': i + 1, 'n_clusters': best_n_clusters[i], 'inertia_dropdown': round(diff[best_n_clusters[i] - 3], 2)})
        
        return resp_data

