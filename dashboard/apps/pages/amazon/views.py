from django.shortcuts import render, redirect
from django.views import generic
from ..crawler.models import Busqueda

import requests
from datetime import  datetime
import django_excel as excel
from bs4 import BeautifulSoup

from .models import ProductoAmazon

from ..crawler.views import CrawlerWeb
from ..crawler.models import Link


# Create your views here.
class IndexView(generic.View):
    """
        IndexView:
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
        query = self.request.POST['query']
        num_paginas = self.request.POST['num_paginas']

        crawler = CrawlerWeb()
        crawler.setUrl('https://www.amazon.com/-/es/')
        crawler.setElement(by='field-keywords', findby=0)
        df = crawler.e_commerceAmz(keys=[query], n_result=num_paginas)
        df['pagina'] = 2

        # guardar historial de busqueda
        id_busqueda = self.buscarid()
        busqueda = Busqueda(id_busqueda=id_busqueda, texto=query, n_paginas=num_paginas, sitios='amazon')
        busqueda.save()
        cont = 0
        for i in df.index:
            titulo = df["titulo"][i]
            url = df["url"][i]
            pagina = df["pagina"][i]
            cont = cont + 1
            if pagina == 2:
                link = Link(id_busqueda=id_busqueda, id_link=cont, url=url, buscador='Amazon')
                link.save()
                self.datosamazon(url, id_busqueda, cont)

        # productos = obtener_datos(df, id_busqueda)
        # contexto = {'productos': productos}

        return redirect('app:pages:amazon-resultados')

    def buscarid(self):
        historia = Busqueda.objects.all()

        if len(historia) == 0:
            return 1
        else:
            valor = len(historia) + 1
            return valor

    def datosamazon(self, link, id_bus, id_pro):

        HEADERS = ({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'
        })

        url = link
        id_busqueda = id_bus
        id_producto = id_pro

        nuevo = []

        webpage = requests.get(url, headers=HEADERS)

        soup = BeautifulSoup(webpage.content, "lxml")

        title = soup.find_all("span", attrs={"id": 'productTitle'})
        titulo = " "
        if len(title) > 0:
            titul = title[0].string
            titulo = titul.replace("\n", "")
            titulo = titulo.replace("\t", "")
            if titulo != " ":
                nuevo.append(titulo)

        price = soup.find_all("span", attrs={'id': 'price_inside_buybox'})
        precio = " "
        if len(price) > 0:
            precio = price[0].string
        nuevo.append(precio)

        ubicaciones = soup.find_all("a", attrs={'id': 'sellerProfileTriggerId'})
        ubicacion = " "
        if len(ubicaciones) > 0:
            ubicacion = ubicaciones[0].string
        nuevo.append(ubicacion)

        descripciones = soup.find_all('span', class_="a-list-item")
        descripcion = " "
        if len(descripciones) > 28:
            for i in range(22, 27, 1):
                descripcion = descripcion + " " + descripciones[i].text
        nuevo.append(descripcion)

        if len(nuevo) == 4:
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

            producto = ProductoAmazon(id_busqueda=id_busqueda, id_producto=id_producto, titulo=titulo, precio=precio,
                                      ubicacion=ubicacion, descripcion=descripcion, url=url)
            producto.save()
        return None


class AmazonResultados(generic.View):
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
            return excel.make_response(sheet, "csv", file_name="OLX-" + strToday + ".csv")

