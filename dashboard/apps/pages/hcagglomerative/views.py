from django.views import generic
from django.http import JsonResponse
import pandas as pd
from pytrends.request import TrendReq
import datetime
from django.urls import reverse
import urllib
from django.shortcuts import render, redirect

from .utils import clusterize


# Create your views here.
class IndexView(generic.View):
    """
    Clase para la pagina principal para mandar a clusterizar
    """
    def get(self, *args, **kwargs):
        
        
        return render(self.request, 'hcagglomerative/base.html')

    

    def post(self, *args, **kwargs):

        context = clusterize(self.request.POST)
        
        self.request.session['n_clusters'] = []
        
        for i, c in enumerate(context.items()):
            self.request.session['n_clusters'].append(c[1])
        
        return redirect('app:pages:clusteringResults')