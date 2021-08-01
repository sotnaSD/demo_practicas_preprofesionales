from django.shortcuts import render
from django.views import generic

from .utils import getDataStructure

import datetime


# Create your views here.
class IndexView(generic.View):
    """
    Clase para la pagina principal para visualizar la estructura de los datos
    """
    
    
    def get(self, *args, **kwargs):
        
        data_structure = getDataStructure()
        context = {
            'inertias_file_name': data_structure["inertias_file_name"],
            'resp_data': data_structure["resp_data"],
            'silhouette_file_name': data_structure['silhouette_file_name']
        }
        
        # data_structure = getDataStructure()
        # context = {
        #     'inertias_file_name': "images/inertias/inercias_2_30-1625072608950.png",
        #     'resp_data': {'n_docs': 124, 'var_dropdown': 1.02, 'avg_dropdown': 1.53, 'best_n_clusters': [{'ranking': 1, 'n_clusters': 3, 'inertia_dropdown': 4.34}, {'ranking': 2, 'n_clusters': 5, 'inertia_dropdown': 3.95}, {'ranking': 3, 'n_clusters': 4, 'inertia_dropdown': 3.83}, {'ranking': 4, 'n_clusters': 8, 'inertia_dropdown': 3.57}]},
        #     'silhouette_file_name': 'images/silhouettes/silhouette_score-1625072601057.png'
        # }
        
        return render(self.request, 'data_structure_analysis/base.html', context)
 
        