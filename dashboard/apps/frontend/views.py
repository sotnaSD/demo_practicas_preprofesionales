from django.shortcuts import render
from django.db.models import Sum
from django.views import generic

# importacion de modelos de cada una de las plataformas
from ..pages.mercadolibre.models import MercadoLibre
from ..pages.twitter.models import Tweet
from ..pages.youtube.models import YoutubeVideo
from ..pages.youtube.models import YoutubeComentario
from .models import TerminoBusqueda
# importacion de una libreria necesaria
import json

# vista del frontend 
class IndexView(generic.TemplateView):

    def get(self, *args, **kwargs):
        # consulta de datos de cada una de la plataforma
        mercadolibre = MercadoLibre.objects.all()
        tweet = Tweet.objects.all()
        youtubeVideo = YoutubeVideo.objects.all()
        youtubeComentario = YoutubeComentario.objects.all()

        # consulta de datos de los terminos de busqueda
        terminoBusqueda = TerminoBusqueda.objects.all()

        # construccion de un diccionario de cada una de las plataformas
        datos = [
            {
                "nombre": "Facebook",
                "valor": 0,
                "class_icons": "fab fa-facebook-square fa-1x"
            },
            {
                "nombre": "Instagram",
                "valor": 0,
                "class_icons": "fab fa-instagram fa-1x"
            },
            {
                "nombre": "Twitter",
                "valor": len(tweet),
                "class_icons": "fab fa-twitter fa-1x"
            },
            {
                "nombre": "Youtube ",
                "valor": len(youtubeComentario) + len(youtubeVideo),
                "class_icons": "fab fa-youtube fa-1x"
            },
            {
                "nombre": "Google",
                "valor": 0,
                "class_icons": "fab fa-google fa-1x"
            },
            {
                "nombre": "Mercado Libre",
                "valor": len(mercadolibre),
                "class_icons": "fas fa-shopping-cart fa-1x"
            },
            {
                "nombre": "OLX",
                "valor": 0,
                "class_icons": "fas fa-fw fa-chart-area fa-1x"
            }]
        # contexto con los parametros necesarios para el template frontend
        context = {
            "total_datos": sum(list([list(i.values())[1] for i in datos])),
            "datos": json.dumps(datos),
            "orden_datos": self.ordenar_vect_dict(datos),
            "num_terminos_busqueda": terminoBusqueda.count(),
            "num_solicitudes": terminoBusqueda.aggregate(suma=Sum("numero_consulta")),
            "orden_terminos": terminoBusqueda.order_by("-numero_consulta")
        }
        return render(self.request, "frontend/base.html", context)

    def ordenar_vect_dict(self, diccionario):
        """
            Metodo para ordenar datos del diccionario segun su valor
        """

        valores_ordenados = sorted([(list(plataforma.values())[1])
                                    for plataforma in diccionario],  reverse=True)
        vect_ordenado = []
        for valor in valores_ordenados:
            for plataforma in diccionario:
                if list(plataforma.values())[1] == valor:
                    vect_ordenado.append(plataforma)
                    diccionario.remove(plataforma)
                    break
        return vect_ordenado
