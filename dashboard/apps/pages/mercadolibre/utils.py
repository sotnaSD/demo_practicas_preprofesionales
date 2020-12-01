import requests


def getPaisMercadoLibre():
    """
    Metodo para obtener todos los paises de mercado libre =
    """
    # obtener paises
    sites_id = requests.get('https://api.mercadolibre.com/sites')
    paises = {}
    for site_id in sites_id.json():
        paises[site_id['id']] = site_id['name']
    return paises


def getCategoryMercadoLibre(id_pais):
    """
    Metodo para obtener categoria de un pais en mercado libre
    """
    # obtener paises
    query = 'https://api.mercadolibre.com/sites/' + str(id_pais).split('-')[0] + '/categories'
    datos_categories = requests.get(query)
    categorias = {}
    for dato_category in datos_categories.json():
        categorias[dato_category['id']] = dato_category['name']
    return categorias


def getTrendsMercadoLibre(id_pais, id_categoria):
    """
    metodo para obtener los datos tendencia de acuerdo a un pais y una categoria
    """
    # Extracción de tendencias en  Ecuador para categoria Ropa y Accesorios
    query = 'https://api.mercadolibre.com/trends/' + id_pais + '/' + id_categoria
    datos_trends = requests.get(query)
    return datos_trends
