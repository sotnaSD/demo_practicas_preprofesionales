from datetime import  datetime
import django_excel as excel

import requests
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.views import generic

# Create your views here.
from ..crawler.models import Busqueda, Link
from ..crawler.views import CrawlerWeb
from ..olx.models import ProductoOlx


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

        crawler = CrawlerWeb()
        df = crawler.e_commerceOLX(key=query, n_result=num_paginas)
        df['pagina'] = 0

        # guardar historial de busqueda
        id_busqueda = self.buscarid()
        busqueda = Busqueda(id_busqueda=id_busqueda, texto=query, n_paginas=num_paginas, sitios='olx')
        busqueda.save()
        cont = 0

        for i in df.index:
            titulo = df["titulo"][i]
            url = df["url"][i]
            pagina = df["pagina"][i]
            cont = cont + 1
            if pagina == 0:
                link = Link(id_busqueda=id_busqueda, id_link=cont, url=url, buscador='OLX')
                link.save()
                self.datosOlx(url, id_busqueda, cont)

        return redirect('app:pages:olx-resultados')

    def buscarid(self):
        historia = Busqueda.objects.all()

        if len(historia) == 0:
            return 1
        else:
            valor = len(historia) + 1
            return valor

    def datosOlx(self, link, id_bus, id_pro):
        url = link
        id_busqueda = id_bus
        id_producto = id_pro

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        nuevo = []

        titulos = soup.find_all('h1', class_='_3rJ6e')
        if len(titulos) > 0:
            titulo = titulos[0].text
            titulo = titulo.replace("\n", "")
            titulo = titulo.replace("\t", "")
            nuevo.append(titulo)

        precios = soup.find_all('span', class_='_2xKfz')
        if len(precios) > 0:
            precio = precios[0].text
            nuevo.append(precio)

        ubicaciones = soup.find_all('span', class_='_2FRXm')

        if len(ubicaciones) > 0:
            ubicacion = ubicaciones[0].text
            nuevo.append(ubicacion)

        descripciones = soup.find_all('p', class_="")

        if len(descripciones) > 0:
            descripcion = ""
            for i in descripciones:
                descripcion = descripcion + "\n" + i.text
            nuevo.append(descripcion)

        if len(nuevo) > 0:
            nuevo.append(link)
            # datos.append(nuevo)
            # print('***********************************')
            # print(id_busqueda)
            # print(id_producto)
            # print(titulo)
            # print(precio)
            # print(ubicacion)
            # print(descripcion)
            # print(url)
            # print('***********************************')
            producto = ProductoOlx(id_busqueda=id_busqueda, id_producto=id_producto, titulo=titulo, precio=precio,
                                   ubicacion=ubicacion, descripcion=descripcion, url=url)
            producto.save()


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
