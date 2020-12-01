from datetime import datetime
import django_excel as excel

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.views import generic
from ...frontend.models import TerminoBusqueda

# Create your views here.
from ..crawler.models import Busqueda, Link
from ..crawler.views import CrawlerWeb
from ..olx.models import ProductoOlx

from .models import ProductoOlx
from .utils import start_crawler


class IndexView(generic.View):
    def get(self, *args, **kwargs):
        datos = ProductoOlx.objects.all()
        name_columns = ProductoOlx._meta.fields
        # parametros para el template tabla.html
        context = {
            'num_registros': datos.count(),
            'num_parametros': len(name_columns),
        }
        return render(self.request, 'olx/base.html', context)

    def post(self, *args, **kwargs):
        # print(self.request.POST)
        query = self.request.POST['query']
        num_paginas = self.request.POST['num_paginas']

        start_crawler(query, num_paginas)
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

        return redirect('app:pages:olx-resultados')


class OlxResultados(generic.View):
    def get(self, *args, **kwargs):
        datos = ProductoOlx.objects.all()
        name_columns = ProductoOlx._meta.fields
        # parametros para el template tabla.html
        context = {
            'num_registros': datos.count(),
            'num_parametros': len(name_columns),
            'datos': datos
        }
        return render(self.request, 'olx/resultados.html', context)

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
            results = ProductoOlx.objects.all()
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
            return excel.make_response(sheet, "csv", file_name="OLX-" + strToday + ".csv")
