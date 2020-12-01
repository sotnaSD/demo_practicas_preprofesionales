from ..crawler.models import Busqueda

import requests
from bs4 import BeautifulSoup

from .models import ProductoOlx

from ..crawler.views import CrawlerWeb
from ..crawler.models import Link


def start_crawler(query, num_paginas):
    crawler = CrawlerWeb()
    df = crawler.e_commerceOLX(key=query, n_result=num_paginas)
    df['pagina'] = 0

    # guardar historial de busqueda
    id_busqueda = buscarid()
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
            datosOlx(url, id_busqueda, cont)

    return None


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
