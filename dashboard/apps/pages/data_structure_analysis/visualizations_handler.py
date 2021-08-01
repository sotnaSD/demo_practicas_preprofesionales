import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_samples
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.cm as cm
from wordcloud import WordCloud
from itertools import compress

import time

class VisualizationHandler():
    def __init__(self):
        pass
    
    def generate_word_clouds(self, y, nClusters, clean_corpus):
        file_names = {}

        for k in range(nClusters):
            cluster_text = ' '.join(doc for doc in list(compress(clean_corpus, y == k)))
            wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white").generate(cluster_text)
            plt.imshow(wordcloud, interpolation='bilinear', aspect='auto')
            plt.axis("off")
            
            ms_time = round(time.time() * 1000)
            word_cloud_file_name = f'cluster_{k}'
            file_path_c = f"dashboard/static/images/word_clouds/{word_cloud_file_name}-{ms_time}.png"
            file_path_s = f"images/word_clouds/{word_cloud_file_name}-{ms_time}.png"
            plt.tight_layout(pad=0)
            plt.savefig(f'./{file_path_c}', format="png")
            file_names[str(k)] = file_path_s
            
        return file_names
    
    def generate_inertias_plot(self, max_nb_clusters, min_nb_clusters, encoded_data):
        # Plot the inertias
        inercias = np.zeros(shape=(max_nb_clusters - min_nb_clusters + 1,))
        for i in range(min_nb_clusters, max_nb_clusters + 1):
            km = KMeans(n_clusters=i, random_state=1000) # It uses by default KMeans ++
            km.fit(encoded_data)
            inercias[i - min_nb_clusters] = km.inertia_

        _, ax = plt.subplots(figsize=(12, 7))
        ax.plot(np.arange(2, max_nb_clusters + 1), inercias)
        ax.set_xlabel('Número de clusters')
        ax.set_ylabel('Inercia')
        ax.set_xticks(np.arange(2, max_nb_clusters + 1))
        ax.grid()
        
        ms_time = round(time.time() * 1000)
        inertias_file_name = f"inercias_{min_nb_clusters}_{max_nb_clusters}"
        file_path_c = f"dashboard/static/images/inertias/{inertias_file_name}-{ms_time}.png"
        file_path_s = f"images/inertias/{inertias_file_name}-{ms_time}.png"
        plt.tight_layout(pad=0)
        plt.savefig(f'./{file_path_c}', format="png")
        return file_path_s
    
    def generate_silhouette_score(self, best_n_clusters, encoded_data):
        _, ax = plt.subplots(2, 2, figsize=(15, 10))
        nb_clusters = best_n_clusters
        mapping = [(0, 0), (0, 1), (1, 0), (1, 1)]
        for i, n in enumerate(nb_clusters):
            km = KMeans(n_clusters=n, random_state=1000)
            Y = km.fit_predict(encoded_data)
            silhouette_values = silhouette_samples(encoded_data, Y)
            ax[mapping[i]].set_xticks([-0.15, 0.0, 0.25, 0.5, 0.75, 1.0])
            ax[mapping[i]].set_yticks([])
            ax[mapping[i]].set_title('%d clusters' % n)
            ax[mapping[i]].set_xlim([-0.15, 1])
            ax[mapping[i]].grid()
            y_lower = 20

            for t in range(n):
                ct_values = silhouette_values[Y == t]
                ct_values.sort()
                y_upper = y_lower + ct_values.shape[0]
                color = cm.Accent(float(t) / n)
                ax[mapping[i]].fill_betweenx(np.arange(y_lower, y_upper), 0, ct_values, facecolor=color, edgecolor=color)
                y_lower = y_upper + 20

        silhouette_file_name = "silhouette_score"
        ms_time = round(time.time() * 1000)
        file_path_c = f"dashboard/static/images/silhouettes/{silhouette_file_name}-{ms_time}.png"
        file_path_s = f"images/silhouettes/{silhouette_file_name}-{ms_time}.png"
        plt.tight_layout(pad=0)
        plt.savefig(f'{file_path_c}', format="png")
        return file_path_s
        