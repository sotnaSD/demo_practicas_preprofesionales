import pandas as pd

from .visualizations_handler import VisualizationHandler
from .cleaner import Cleaner
from .transformer import Transformer
from .models_handler import ModelHandler

def clusterize(request_data):
    
    
    cleaner = Cleaner()
    transformer = Transformer()
    visualization_handler = VisualizationHandler()
    models_handler = ModelHandler()
    
    raw_df = pd.read_csv('docs.csv')
    clean_df = cleaner.clean_data(raw_df)
    encoded_data = transformer.encode_data(request_data["codification"], clean_df["Docs"])
    
    y = models_handler.get_clusters(request_data, encoded_data)
    word_clouds = visualization_handler.generate_word_clouds(y, int(request_data["nClusters"]), clean_df["Docs"])
    
    return word_clouds
    
    