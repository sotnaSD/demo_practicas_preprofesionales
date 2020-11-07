from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
import pandas as pd
from pytrends.request import TrendReq
import datetime
pytrend = TrendReq(hl='es-EC', tz=360)
from ...frontend.models import TerminoBusqueda
from django.views.generic import View
# Create your views here.
class IndexView(generic.TemplateView):
    """
    IndexView:
    """
    module = 'IndexView'
    template_name = 'google/base.html'

def obtenerTrends(request):
    palabraClave = request.GET.get('palabraClave', None)
    palabraClave2 = request.GET.get('palabraClave2', None)
    timeframe = request.GET.get('fecha', None)
    #para guardar los terminos de busqueda
    # comparacion de si exite algun temino solo actualiza el numero de consulta
    if TerminoBusqueda.objects.filter(nombre=palabraClave).exists():
        datos = TerminoBusqueda.objects.filter(nombre=palabraClave)
        TerminoBusqueda.objects.filter(nombre=palabraClave).update(
            numero_consulta=datos[0].numero_consulta + 1)
    else:
        terminos_busqueda = TerminoBusqueda(
            nombre=palabraClave, numero_consulta=1)
        terminos_busqueda.save()

    if TerminoBusqueda.objects.filter(nombre=palabraClave2).exists():
        datos = TerminoBusqueda.objects.filter(nombre=palabraClave2)
        TerminoBusqueda.objects.filter(nombre=palabraClave2).update(
            numero_consulta=datos[0].numero_consulta + 1)
    else:
        terminos_busqueda = TerminoBusqueda(
            nombre=palabraClave2, numero_consulta=1)
        terminos_busqueda.save()

    # formamos el build de la consulta
    pytrend = TrendReq(hl='es-EC', tz=360)
    keywords = ['Edredones', 'Mascarillas']
    pytrend.build_payload(
        kw_list=[palabraClave,palabraClave2],
        cat=0,
        # timeframe='today 3-m',
        timeframe=timeframe,
        geo='EC',
        gprop='')
    data = pytrend.interest_over_time()
    data = data.drop(labels=['isPartial'], axis='columns')
    data = data.reset_index()
    fechas = data['date']
    trend = data.iloc[:,1]
    trend2 = data.iloc[:, 2]



    #para el interes por region
    data = pytrend.interest_by_region()
    data = data.reset_index()
    palabra1 = data.iloc[:, [0, 1]]
    palabra1 = palabra1.sort_values(by=palabra1.columns[1], ascending=False).head(10)
    palabra2 = data.iloc[:, [0, 2]]
    palabra2 = palabra2.sort_values(by=palabra2.columns[1], ascending=False).head(10)
    interesRegion = palabra1.iloc[:, 1]
    label1 = palabra1.iloc[:, 0]
    interesRegion2 = palabra2.iloc[:, 1]
    label2 = palabra2.iloc[:, 0]

    response = {
        'fechas': fechas.dt.date.unique().tolist(),
        'trend': trend.to_list(),
        'trend2': trend2.to_list(),
        'interesRegion': interesRegion.tolist(),
        'label1': label1.to_list(),
        'interesRegion2': interesRegion2.tolist(),
        'label2': label2.to_list(),

    }
    return JsonResponse(response)

def obtenerTrendsRegion(request):
    palabraClave = request.GET.get('palabraClave', None)
    palabraClave2 = request.GET.get('palabraClave2', None)
    timeframe = request.GET.get('fecha', None)
    # En los ultimos tres meses
    pytrend = TrendReq(hl='es-EC', tz=360)
    pytrend.build_payload(
        kw_list=[palabraClave,palabraClave2],
        cat=0,
        # timeframe='today 3-m',
        timeframe=timeframe,
        geo='EC',
        gprop='')
    data = pytrend.interest_by_region()
    data = data.reset_index()
    palabra1 = data.iloc[:, [0, 1]]
    palabra1 = palabra1.sort_values(by=data.columns[1], ascending=False).head(10)
    palabra2 = data.iloc[:, [0, 2]]
    palabra2 = palabra2.sort_values(by=data.columns[1], ascending=False).head(10)
    interesRegion = palabra1.iloc[:,1]
    print(interesRegion)
    label = palabra1.iloc[:,0]
    interesRegion2 = palabra2.iloc[:, 1]
    label2 = palabra2.iloc[:, 0]
    #data.to_csv('edr_VS_masc.csv', encoding='utf_8_sig')
    response = {
        'interesRegion': interesRegion.tolist(),
        'label': label.to_list(),
    }
    return JsonResponse(response)
