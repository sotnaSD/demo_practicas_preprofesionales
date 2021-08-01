import pandas as pd

# from .visualizations_handler import VisualizationHandler
# from .cleaner import Cleaner
# from .transformer import Transformer
# from .optimizer import Optimizer


def getModels():
    pass
    # raw_df = pd.read_csv('docs.csv')
    # cleaner = Cleaner()
    # clean_df = cleaner.clean_data(raw_df)
    # transformer = Transformer()
    # optimizer = Optimizer()
    # visualization_handler = VisualizationHandler()
    
    # encoded_data = transformer.encode_data("TF-IDF", clean_df["Docs"])
    
    # data_structure, best_n_clusters = optimizer.get_data_structure(encoded_data)
    # silhouette_file_name = visualization_handler.generate_silhouette_score(best_n_clusters, encoded_data)
    
    # inertias_file_name = visualization_handler.generate_inertias_plot(30, 2, encoded_data)
    
    # return {"inertias_file_name": inertias_file_name, 'resp_data': data_structure, 'silhouette_file_name': silhouette_file_name}
    
    
    # return {"inertias_file_name": url_base + inertias_file_name, 'resp_data': data_structure, 'silhouette_file_name': url_base + silhouette_file_name}



# def getCategoryMercadoLibre(id_pais):
#     """
#     Metodo para obtener categoria de un pais en mercado libre
#     """
#     # obtener paises
#     query = 'https://api.mercadolibre.com/sites/' + str(id_pais).split('-')[0] + '/categories'
#     datos_categories = requests.get(query)
#     categorias = {}
#     for dato_category in datos_categories.json():
#         categorias[dato_category['id']] = dato_category['name']
#     return categorias


# def getTrendsMercadoLibre(id_pais, id_categoria):
#     """
#     metodo para obtener los datos tendencia de acuerdo a un pais y una categoria
#     """
#     # Extracción de tendencias en  Ecuador para categoria Ropa y Accesorios
#     query = 'https://api.mercadolibre.com/trends/' + id_pais + '/' + id_categoria
#     datos_trends = requests.get(query)
#     return datos_trends
