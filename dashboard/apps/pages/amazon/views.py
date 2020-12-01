from django.shortcuts import render, redirect
from django.views import generic
from ..crawler.models import Busqueda

import requests
from datetime import  datetime
import django_excel as excel
from bs4 import BeautifulSoup

from .models import ProductoAmazon
from .utils import start_crawler
from ...frontend.models import TerminoBusqueda


# Create your views here.
class IndexView(generic.View):
    """
        IndexView: Clase para la ventana de Amazon
    """

    def get(self, *args, **kwargs):
        # return template
        datos = ProductoAmazon.objects.all()
        name_columns = ProductoAmazon._meta.fields
        # parametros para el template tabla.html
        context = {
            'num_registros': datos.count(),
            'num_parametros': len(name_columns),
        }
        return render(self.request, 'amazon/base.html', context)

    def post(self, *args, **kwargs):
        # print(self.request.POST)
        query = self.request.POST['query'].split(',')
        num_paginas = self.request.POST['num_paginas']
        start_crawler(query[0], num_paginas)

        # guardar consulta -- para historial
        for i in query:
            # comparacion de si exite algun temino solo actualiza el numero de consulta
            if TerminoBusqueda.objects.filter(nombre=i).exists():
                datos = TerminoBusqueda.objects.filter(nombre=i)
                TerminoBusqueda.objects.filter(nombre=i).update(
                    numero_consulta=datos[0].numero_consulta + 1)
            else:
                terminos_busqueda = TerminoBusqueda(
                    nombre=i, numero_consulta=1)
                terminos_busqueda.save()

        ######

        return redirect('app:pages:amazon-resultados')



class AmazonResultados(generic.View):
    """
    Clases para mostrar los resultados de la consulta Amazon
    """
    def get(self, *args, **kwargs):
        datos = ProductoAmazon.objects.all()
        name_columns = ProductoAmazon._meta.fields
        # parametros para el template tabla.html
        context = {
            'num_registros': datos.count(),
            'num_parametros': len(name_columns),
            'datos':datos
        }
        return render(self.request, 'amazon/resultados.html', context)

    def post(self, *args, **kwargs):
        # exportar datos como csv
        if self.request.method == "POST":
            export = []
            # Se agregan los encabezados de las columnas
            export.append([
                'id_busqueda',
                'id_producto',
                'titulo',
                'precio',
                'ubicacion',
                'descripcion',
                'url',
            ])

            # Se obtienen los datos de la tabla o model y se agregan al array
            results = ProductoAmazon.objects.all()
            for result in results:
                # agregar las filas
                export.append([
                    result.id_busqueda,
                    result.id_producto,
                    result.titulo,
                    result.precio,
                    result.ubicacion,
                    result.descripcion,
                    result.url,
                ])

            # Obtenemos la fecha para agregarla al nombre del archivo
            today = datetime.now()
            strToday = today.strftime("%Y%m%d")

            # se transforma el array a una hoja de calculo en memoria
            sheet = excel.pe.Sheet(export)

            # se devuelve como "Response" el archivo para que se pueda "guardar"
            # en el navegador, es decir como hacer un "Download"
            return excel.make_response(sheet, "csv", file_name="Amazon-" + strToday + ".csv")

