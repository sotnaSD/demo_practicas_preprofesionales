from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
import pandas as pd
from pytrends.request import TrendReq
import datetime

# Create your views here.
class IndexView(generic.View):
    """
    Clase para la pagina principal de los resultados
    """
    def get(self, *args, **kwargs):
        # obtencion de los datos de la base de datos
        # parametros para el template tabla.html

        # return template principal con parametros

        
        return render(self.request, 'clustering_results/base.html')