from ..crawler.models import Busqueda

import requests
from bs4 import BeautifulSoup

from .models import ProductoAmazon

from ..crawler.views import CrawlerWeb
from ..crawler.models import Link


def start_crawler(query, num_paginas):
    crawler = CrawlerWeb()
    crawler.setUrl('https://www.amazon.com/-/es/')
    crawler.setElement(by='field-keywords', findby=0)
    df = crawler.e_commerceAmz(keys=[query], n_result=num_paginas)
    df['pagina'] = 2

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
        if pagina == 2:
            link = Link(id_busqueda=id_busqueda, id_link=cont, url=url, buscador='Amazon')
            link.save()
            datosamazon(url, id_busqueda, cont)

    return None


def buscarid():
    historia = Busqueda.objects.all()

    if len(historia) == 0:
        return 1
    else:
        valor = len(historia) + 1
        return valor


def datosamazon( link, id_bus, id_pro):
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
        producto = ProductoAmazon(id_busqueda=id_busqueda, id_producto=id_producto, titulo=titulo, precio=precio,
                                  ubicacion=ubicacion, descripcion=descripcion, url=url)
        producto.save()
    return None
