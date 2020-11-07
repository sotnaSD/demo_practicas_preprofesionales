import requests
pais='' 
categoria=''

def getPaisMercadoLibre():
    # obtener paises
    sites_id = requests.get('https://api.mercadolibre.com/sites')
    paises={}
    for site_id in sites_id.json():
        paises[site_id['id']]=site_id['name']
    return paises


def getCategoryMercadoLibre(id_pais):
    # obtener paises
    query='https://api.mercadolibre.com/sites/'+str(id_pais).split('-')[0]+'/categories'
    datos_categories = requests.get(query)
    categorias={}
    for dato_category in datos_categories.json():
        categorias[dato_category['id']]=dato_category['name']
    return categorias

def getTrendsMercadoLibre(id_pais,id_categoria):
    # Extracción de tendencias en  Ecuador para categoria Ropa y Accesorios
    query='https://api.mercadolibre.com/trends/'+id_pais+'/'+id_categoria
    datos_trends = requests.get(query)
    return datos_trends

