from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
import pandas as pd
from pytrends.request import TrendReq
import datetime
from django.urls import reverse
import urllib
from django.shortcuts import render, redirect

import os



# Create your views here.
class IndexView(generic.View):
    """
    Clase para la pagina principal para mandar a clusterizar
    """
    def get(self, *args, **kwargs):
        
        
        return render(self.request, 'update_db/base.html')
    

    def post(self, *args, **kwargs):
        
        print("llego aqui ")
        

        os.system('python dashboard/script/export_data.py')
        
        return render(self.request, 'update_db/base.html')
