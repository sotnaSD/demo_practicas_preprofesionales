from django.shortcuts import render, redirect
from django.views import generic
# importacion  form y conexion con la api
from .utils import getAPI
from .forms import TwitterForm
# importacion de modelos de bases de datos
from .models import Tweet
from ...frontend.models import TerminoBusqueda
# importacion de librerias necesarias
import tweepy
from datetime import datetime
import django_excel as excel

# View de la plataforma Twiiter
class IndexView(generic.View):
    # IndexView:

    def get(self, *args, **kwargs):
        # obtencion de los datos de la base de datos
        datos = Tweet.objects.all()
        name_columns = Tweet._meta.fields
        context = {
            'num_registros': datos.count(),
            'num_parametros': len(name_columns),
        }
        # return template principal con parametros
        return render(self.request, 'twitter/base.html', context)

    def post(self, *args, **kwargs):
        twitterForm = TwitterForm(self.request.POST or None)
        if twitterForm.is_valid():
            api = getAPI(self.request)
            fecha_inicio = twitterForm.cleaned_data['input_fecha_inicio']
            fecha_fin = twitterForm.cleaned_data['input_fecha_fin']
            query = twitterForm.cleaned_data['input_palabras_claves'].split(',')
            ubicacion = twitterForm.cleaned_data['input_ubicacion']
            idioma = twitterForm.cleaned_data['input_idioma']

            tweets=None
            #validacion si hay parametro ubicacion  
            if len(ubicacion)>0:
                try: 
                    places = api.geo_search(query=ubicacion, granularity="country")
                    ubicacion = places[0].id
                except Exception as e:
                    # poner por defecto pais el ecuador
                    ubicacion = '4e43cac8250a8b20'
                    print('Se paso a pais por defecto Ecuador')
                # obtencion de tweets mediante la api con los parametro obtenidos del frontend 
                tweets=tweepy.Cursor(api.search,
                                     lang=idioma,
                                     q=query,
                                     since=fecha_inicio,
                                     until=fecha_fin,
                                     tweet_mode='extended').items()
            else:
                # obtencion de tweets mediante la api con los parametro obtenidos del frontend 
                tweets=tweepy.Cursor(api.search,
                                     lang=idioma,
                                     q=query,
                                     since=fecha_inicio,
                                     until=fecha_fin,
                                     tweet_mode='extended').items()
            # recorridos por cada tweet y guardado de los datos
            for tweet in tweets:
                # print('********************')
                tweet = Tweet(created_at=tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                              userName=tweet.user.name,
                              isVerified=tweet.user.verified,
                              userFollowers_count=tweet.user.followers_count,
                              userFriends_count=tweet.user.friends_count,
                              userFavourites_count=tweet.user.favourites_count,
                              userStatuses_count=tweet.user.statuses_count,
                              tweet_id=tweet.id,
                              tweet=tweet.full_text.replace('\n', ' '),
                              tweetRetweet_count=tweet.retweet_count,
                              tweetFavorite_count=tweet.favorite_count,
                              tweetLocation=tweet._json["user"]["location"]
                              )
                tweet.save()
                
            # guardar cada uno de los terminos de busqueda
            for i in query:
                # comparacion de si exite algun temino solo actualiza el numero de consulta
                if TerminoBusqueda.objects.filter(nombre=i).exists():
                    datos = TerminoBusqueda.objects.filter(nombre=i)
                    TerminoBusqueda.objects.filter(nombre=i).update(
                        numero_consulta=datos[0].numero_consulta+1)
                else:
                    terminos_busqueda = TerminoBusqueda(
                        nombre=i, numero_consulta=1)
                    terminos_busqueda.save()
            return redirect('app:pages:twitter_resultados')
        else:
            # obtencion de los datos de la base de datos
            datos = Tweet.objects.all()
            name_columns = Tweet._meta.fields
            context = {
                'num_registros': datos.count(),
                'num_parametros': len(name_columns),
                'formTweets': twitterForm
            }
            return render(self.request, 'twitter/base.html', context)

class TwitterResultados(generic.View):
    """
    IndexView:
    """
    def get(self, *args, **kwargs):
        # consulta a la base de datos
        datos = Tweet.objects.all()
        name_columns = Tweet._meta.fields
        context = {
            'num_registros': datos.count(),
            'num_parametros': len(name_columns),
            'datos': datos,
            'name_columns': name_columns
        }
        # renderiza el template con cada uno de los paramtros
        return render(self.request, 'twitter/tables.html', context)

    def post(self, *args, **kwargs):
        # exportar datos como csv
        if self.request.method == "POST":
            export = []
            # Se agregan los encabezados de las columnas
            export.append([
                'consulted_at',
                'created_at',
                'userName',
                'isVerified',
                'userFollowers_count',
                'userFriends_count',
                'userFavourites_count',
                'userStatuses_count',
                'tweet_id',
                'tweet',
                'tweetRetweet_count',
                'tweetFavorite_count',
                'tweetLocation', ])

            # Se obtienen los datos de la tabla o model y se agregan al array
            results = Tweet.objects.all()
            for result in results:
                # agregar las filas 
                export.append([
                    result.consulted_at,
                    result.created_at,
                    result.userName,
                    result.isVerified,
                    result.userFollowers_count,
                    result.userFriends_count,
                    result.userFavourites_count,
                    result.userStatuses_count,
                    result.tweet_id,
                    result.tweet,
                    result.tweetRetweet_count,
                    result.tweetFavorite_count,
                    result.tweetLocation
                ])

            # Obtenemos la fecha para agregarla al nombre del archivo
            today = datetime.now()
            strToday = today.strftime("%Y%m%d")

            # se transforma el array a una hoja de calculo en memoria
            sheet = excel.pe.Sheet(export)

            # se devuelve como "Response" el archivo para que se pueda "guardar"
            # en el navegador, es decir como hacer un "Download"
            return excel.make_response(sheet, "csv", file_name="twitter-"+strToday+".csv")
