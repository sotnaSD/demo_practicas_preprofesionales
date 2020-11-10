from django.shortcuts import render
from django.views import generic
from django.http import JsonResponse
import pandas as pd
from pytrends.request import TrendReq
import datetime
pytrend = TrendReq(hl='es-EC', tz=360)
from django.views.generic import View
import django_excel as excel
# Create your views here.
class IndexView(generic.TemplateView):
    """
    IndexView:
    """
    module = 'IndexView'
    template_name = 'google/base.html'

def obtenerTrends(request):
    palabraClave = request.GET.get('palabraClaves', None)
    query = palabraClave.split(',')
    region = request.GET.get('region', None)
    timeframe = request.GET.get('fecha', None)
    # En los ultimos tres meses
    pytrend = TrendReq(hl='es-EC', tz=360)
    keywords = ['Edredones', 'Mascarillas']
    pytrend.build_payload(
        kw_list=query,
        cat=0,
        # timeframe='today 3-m',
        timeframe=timeframe,
        geo=region,
        gprop='')
    data = pytrend.interest_over_time()
    data = data.drop(labels=['isPartial'], axis='columns')
    data = data.reset_index()
    fechas = data['date']
    trends = data.drop(labels=['date'], axis='columns')
     #para el interes por region
    data = pytrend.interest_by_region()
    data = data.reset_index()
    regiones = data["geoName"]
    trendsRegiones = data.drop(labels=['geoName'], axis='columns')
    response = {
        'fechas': fechas.dt.date.unique().tolist(),
        'trends': trends.to_json(),
        'regiones': regiones.tolist(),
        'regiones_trends': trendsRegiones.to_json(),
    }
    return JsonResponse(response)


#para exportar los datos de google trends
def exportarTrends(request):
    palabraClave = request.GET.get('palabraClaves', None)
    query = palabraClave.split(',')
    region = request.GET.get('region', None)
    timeframe = request.GET.get('fecha', None)
    # En los ultimos tres meses
    pytrend = TrendReq(hl='es-EC', tz=360)
    keywords = ['Edredones', 'Mascarillas']
    pytrend.build_payload(
        kw_list=query,
        cat=0,
        # timeframe='today 3-m',
        timeframe=timeframe,
        geo=region,
        gprop='')
    data = pytrend.interest_over_time()
    data = data.drop(labels=['isPartial'], axis='columns')
    data = data.reset_index()
    export = []
    # Se agregan los encabezados de las columnas
    export.append(data.columns.tolist())
    # Se obtienen los datos de la tabla o model y se agregan al array
    for index, row in data.iterrows():
        export.append(row)
    # se transforma el array a una hoja de calculo en memoria
    sheet = excel.pe.Sheet(export)
    # se devuelve como "Response" el archivo para que se pueda "guardar"
    # en el navegador, es decir como hacer un "Download"
    print("asasas")
    return excel.make_response(sheet, "csv", file_name= 'google_trends_data'+(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))+'.csv')