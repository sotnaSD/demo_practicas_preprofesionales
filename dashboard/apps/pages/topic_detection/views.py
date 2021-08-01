from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
import pandas as pd
from pytrends.request import TrendReq
import datetime

from django.shortcuts import render, redirect


# Create your views here.
class IndexView(generic.View):
    """
    Clase para la pagina principal para mandar a clusterizar
    """
    def get(self, *args, **kwargs):
        # obtencion de los datos de la base de datos
        # parametros para el template tabla.html

        # return template principal con parametros
        context = {
            'modelos': ["K-means", "Hierarchical clustering - Agglomerative"],
        }
        
        return render(self.request, 'topic_detection/base.html', context)
    

    def post(self, *args, **kwargs):

        print("*****")
        print(self.request.POST)

        
        return redirect('app:pages:clusteringResults')