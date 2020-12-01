from django.shortcuts import render, redirect
from django.views import generic

from datetime import datetime
import django_excel as excel

from .models import ProductoMercadoLibre
from .utils import start_crawler
from ...frontend.models import TerminoBusqueda


# Create your views here.
class IndexView(generic.View):
    """
        IndexView: clase principal para mercado libre de webscraping
    """

    def get(self, *args, **kwargs):
        datos = ProductoMercadoLibre.objects.all()
        name_columns = ProductoMercadoLibre._meta.fields
        # parametros para el template tabla.html
        context = {
            'num_registros': datos.count(),
            'num_parametros': len(name_columns),
        }
        # return template
        return render(self.request, 'mercadolibre_scraping/base.html', context)

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

        #
        return redirect('app:pages:mercadolibrescraping_resultados')


class MercadoLibreResultados(generic.View):
    """
    Clase principal para resultados de mercado libre de web scraping
    """
    def get(self, *args, **kwargs):
        datos = ProductoMercadoLibre.objects.all()
        name_columns = ProductoMercadoLibre._meta.fields
        # parametros para el template tabla.html
        context = {
            'num_registros': datos.count(),
            'num_parametros': len(name_columns),
            'datos': datos
        }
        # datos = ProductoMercadoLibre.objects.all()
        return render(self.request, 'mercadolibre_scraping/resultados.html', context)

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
            results = ProductoMercadoLibre.objects.all()
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
            return excel.make_response(sheet, "csv", file_name="mercadolibre-publicaciones-" + strToday + ".csv")
