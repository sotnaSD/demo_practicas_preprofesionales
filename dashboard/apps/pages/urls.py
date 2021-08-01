from django.urls import path

import dashboard.apps.pages.facebook.views as facebookViews
import dashboard.apps.pages.instagram.views as instagramViews
import dashboard.apps.pages.twitter.views as twitterViews
import dashboard.apps.pages.mercadolibre.views as mercadoLibreAPIViews
import dashboard.apps.pages.mercadolibre_scraping.views as mercadoLibreScrapingViews
import dashboard.apps.pages.olx.views as olxViews
import dashboard.apps.pages.amazon.views as amazonViews
import dashboard.apps.pages.youtube.views as youtubeViews
import dashboard.apps.pages.google.views as googleViews
import dashboard.apps.pages.pinterest.views as pinterestViews
import dashboard.apps.frontend.views as mainViews

import dashboard.apps.pages.topic_detection.views as tdViews
import dashboard.apps.pages.data_structure_analysis.views as dSAView
import dashboard.apps.pages.clustering_results.views as cRView

import dashboard.apps.pages.kmeans.views as KMView
import dashboard.apps.pages.hcagglomerative.views as HCAView
import dashboard.apps.pages.update_db.views as DBView


app_name = 'pages'

urlpatterns = [
    path('', mainViews.IndexView.as_view(), name='index'),
    path('facebook', facebookViews.IndexView.as_view(), name='facebook'),
    path('instagram', instagramViews.IndexView.as_view(), name='instagram'),
    path('twitter', twitterViews.IndexView.as_view(), name='twitter'),
    path('twitter_resultados', twitterViews.TwitterResultados.as_view(), name='twitter_resultados'),
    path('youtube', youtubeViews.YoutubeParametros.as_view(), name='youtube'),
    path('youtube-resultados/', youtubeViews.YoutubeVideoView.as_view(), name='youtube_resultados'),
    path('youtube-resultados-comentarios/', youtubeViews.YoutubeComentariosView.as_view(),
         name='youtube_resultados_comentarios'),
    path('youtube-resultados-videos/exportar/', youtubeViews.exportarVideos, name='youtube-videos-exportar'),
    path('youtube-resultados-comentarios/exportar/', youtubeViews.exportarComentarios,
         name='youtube-comentarios-exportar'),
    path('obtener-trends', googleViews.obtenerTrends, name='obtener-trends'),
    path('obtener-trends/exportar/', googleViews.exportarTrends, name='exportar-trends'),

    path('olx', olxViews.IndexView.as_view(), name='olx'),
    path('olx-resultados', olxViews.OlxResultados.as_view(), name='olx-resultados'),

    path('amazon', amazonViews.IndexView.as_view(), name='amazon'),
    path('amazon-resultados', amazonViews.AmazonResultados.as_view(), name='amazon-resultados'),

    path('google', googleViews.IndexView.as_view(), name='google'),

    path('mercadolibre_api', mercadoLibreAPIViews.IndexView.as_view(), name='mercadolibre_api'),
    path('mercadolibre_resultados', mercadoLibreAPIViews.MercadoLibreResutlados.as_view(),
         name='mercadolibre_resultados'),

    path('mercadolibre_scraping', mercadoLibreScrapingViews.IndexView.as_view(), name='mercadolibre_scraping'),
    path('mercadolibrescraping_resultados', mercadoLibreScrapingViews.MercadoLibreResultados.as_view(),
         name='mercadolibrescraping_resultados'),

    path('pinterest', pinterestViews.IndexView.as_view(), name='pinterest'),
    path('pinterest_resultados', pinterestViews.PinterestResultados.as_view(),
         name='pinterest-resultados'),
    
    path('topic_detection', tdViews.IndexView.as_view(), name='topic_detection'),
    path('data_structure_analysis', dSAView.IndexView.as_view(), name='data_structure_analysis'),
    path('clusteringResults', cRView.IndexView.as_view(), name='clusteringResults'),
    
    path('kmeans', KMView.IndexView.as_view(), name='kmeans'),
    
    path('hcagglomerative', HCAView.IndexView.as_view(), name='hcagglomerative'),
    
    path('update_db', DBView.IndexView.as_view(), name='update_db'),
]
