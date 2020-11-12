
from ..crawler.models import Busqueda

import requests
from bs4 import BeautifulSoup

from .models import ProductoMercadoLibre

from ..crawler.views import CrawlerWeb
from ..crawler.models import Link


def start_crawler(query, num_paginas):
    crawler = CrawlerWeb()
    crawler.setUrl('https://listado.mercadolibre.com.ec/')
    crawler.setElement(by='as_word', findby=0)
    df = crawler.e_commerceML(keys=[query], n_result=num_paginas)
    df['pagina'] = 1

    # guardar historial de busqueda
    id_busqueda = buscarid()
    busqueda = Busqueda(id_busqueda=id_busqueda, texto=query, n_paginas=num_paginas, sitios='amazon')
    busqueda.save()
    cont = 0
    for i in df.index:
        titulo = df["titulo"][i]
        url = df["url"][i]
        pagina = df["pagina"][i]
        cont = cont + 1
        if pagina == 1:
            link = Link(id_busqueda=id_busqueda, id_link=cont, url=url, buscador='Mercado Libre')
            link.save()
            datosMercadoLibre(url, id_busqueda, cont)

    # productos = obtener_datos(df, id_busqueda)
    # contexto = {'productos': productos}

    return None


def buscarid():
    historia = Busqueda.objects.all()

    if len(historia) == 0:
        return 1
    else:
        valor = len(historia) + 1
        return valor


def datosMercadoLibre( link, id_bus, id_pro):
    url = link
    id_busqueda = id_bus
    id_producto = id_pro

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    nuevo = []

    titulos = soup.find_all('h1', class_='item-title__primary')
    titulo = " "
    if len(titulos) > 0:
        titulo = titulos[0].text
        titulo = titulo.replace("\n", "")
        titulo = titulo.replace("\t", "")
    nuevo.append(titulo)

    precio = " "
    precios = soup.find_all('span', class_='price-tag-fraction')
    if len(precios) > 0:
        precio = precios[0].text
    nuevo.append(precio)

    ubicaciones = soup.find_all('p', class_='gray')
    ubicacion = " "
    if len(ubicaciones) > 0:
        ubicacion = ubicaciones[0].text
    nuevo.append(ubicacion)

    descripciones = soup.find_all('div', class_="item-description__text")
    descripcion = ""
    if len(descripciones) > 0:
        for i in descripciones:
            descripcion = descripcion + " " + i.text
    nuevo.append(descripcion)

    if len(nuevo) > 0:
        nuevo.append(link)
        # datos.append(nuevo)
        producto = ProductoMercadoLibre(id_busqueda=id_busqueda, id_producto=id_producto, titulo=titulo,
                                        precio=precio,
                                        ubicacion=ubicacion, descripcion=descripcion, url=url)
        producto.save()
    return None