from django.shortcuts import render, redirect
from django.views import generic

# importacion de modelos de bases de datos
from .models import ProductoPinterest, ProductoPinterestComentario
from ..crawler.views import CrawlerWeb
from ...frontend.models import TerminoBusqueda
# importacion de librerias necesarias
from datetime import datetime
import django_excel as excel

# View de la plataforma Twiiter


class IndexView(generic.View):
    """
    Clase para la pagina principal de pinterest
    """
    def get(self, *args, **kwargs):
        # obtencion de los datos de la base de datos
        datos = ProductoPinterestComentario.objects.all()
        name_columns = ProductoPinterestComentario._meta.fields
        # parametros para el template tabla.html
        context = {
            'num_registros': datos.count(),
            'num_parametros': len(name_columns),
        }
        # return template principal con parametros
        return render(self.request, 'pinterest/base.html', context)

    def post(self, *args, **kwargs):
        # print(self.request.POST)
        query = self.request.POST['query'].split(',')
        print(query,'    ====================')
        num_paginas = self.request.POST['num_paginas']
        crawler = CrawlerWeb()
        datos = crawler.pinterest(keys=query, n_result=num_paginas)
        crawler.newDriver()
        datos = crawler.getPinterestUrl(datos)
        print(datos)
        #guardar datos de productos
        for index, fila in datos[0].iterrows():
            dato = ProductoPinterest(
                titulo=fila.titulo,
                url=fila.url,
                descripcion=fila.descripcion,
                url_imagen=fila.img
            )

            dato.save()
            #guarda comentario
            for index, row in datos[1][datos[1].url == fila.url].iterrows():
                comentario = ProductoPinterestComentario(
                    url=dato,
                    comentario=row.comentario
                )
                comentario.save()
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
        return redirect('app:pages:pinterest-resultados')


class PinterestResultados(generic.View):
    """
    IndexView: para la pagina de resultados de pinterest
    """

    def get(self, *args, **kwargs):
        # renderiza el template con cada uno de los paramtros

        datos = ProductoPinterest.objects.all()

        name_columns = ProductoPinterest._meta.fields
        # parametros para el template tabla.html
        context = {
            'num_registros': datos.count(),
            'num_parametros': len(name_columns),
            'datos': datos
        }
        return render(self.request, 'pinterest/resultado.html', context)

    def post(self, *args, **kwargs):
        # exportar datos como csv
        if self.request.method == "POST":
            export = []
            # Se agregan los encabezados de las columnas
            export.append([
                'titulo',
                'descripcion',
                'url',
                'comentario',
                'url imagen'
            ])

            # Se obtienen los datos de la tabla o model y se agregan al array
            results = ProductoPinterest.objects.all()
            for result in results:
                if result.get_comentario.exists():
                    for i in result.get_comentario:
                        export.append([
                            result.titulo,
                            result.descripcion,
                            result.url,
                            i.comentario,
                            result.url_imagen
                        ])
                else:
                    # agregar las filas
                    export.append([
                        result.titulo,
                        result.descripcion,
                        result.url,
                        '',
                        result.url_imagen
                    ])

            # Obtenemos la fecha para agregarla al nombre del archivo
            today = datetime.now()
            strToday = today.strftime("%Y%m%d")

            # se transforma el array a una hoja de calculo en memoria
            sheet = excel.pe.Sheet(export)

            # se devuelve como "Response" el archivo para que se pueda "guardar"
            # en el navegador, es decir como hacer un "Download"
            return excel.make_response(sheet, "csv", file_name="Pinterest-" + strToday + ".csv")
