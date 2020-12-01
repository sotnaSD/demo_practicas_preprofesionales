from django.shortcuts import render
from django.views import generic
from django.views.generic import View
from .forms import YoutubeVideoForm, YoutubeCommentForm
from .models import YoutubeVideo, YoutubeComentario
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from django.conf import settings
from googleapiclient.discovery import build
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv
import unidecode
import datetime
import django_excel as excel
from ...frontend.models import TerminoBusqueda

YOUTUBE_DEVELOPER_KEY = settings.YOUTUBE_DEVELOPER_KEY
YOUTUBE_API_SERVICE_NAME = settings.YOUTUBE_API_SERVICE_NAME
YOUTUBE_API_VERSION = settings.YOUTUBE_API_VERSION


def exportarVideos(request):
    export = []
    # Se agregan los encabezados de las columnas
    export.append(["Fecha de Consulta", "VideoId", "Titulo Video", "Fecha Publicación", "Numero Vistas", "Numero Likes",
                   "Numero Dislikes", "Numero Comentarios"])
    # Se obtienen los datos de la tabla o model y se agregan al array
    results = YoutubeVideo.objects.all()
    for result in results:
        # ejemplo para dar formato a fechas, estados (si/no, ok/fail) o
        # acceder a campos con relaciones y no solo al id
        export.append([
            result.fechaConsulta, result.videoId, result.titulo, result.fechaPublicacion, result.numeroVistas,
            result.numeroLikes,
            result.numeroDisLikes, result.numeroComentarios
        ])
    # se transforma el array a una hoja de calculo en memoria
    sheet = excel.pe.Sheet(export)
    # se devuelve como "Response" el archivo para que se pueda "guardar"
    # en el navegador, es decir como hacer un "Download"
    return excel.make_response(sheet, "csv", file_name='youtube_video_data_analysis' + (
        datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")) + '.csv')


def exportarComentarios(request):
    export = []
    # Se agregan los encabezados de las columnas
    export.append(["Fecha de Consulta", "VideoId", "Fecha Publicacion", "Comentario", "Trend", "Numero Likes",
                   "Comentario Respuestas", "Es Toplevel"])
    # Se obtienen los datos de la tabla o model y se agregan al array
    results = YoutubeComentario.objects.all()
    for result in results:
        # ejemplo para dar formato a fechas, estados (si/no, ok/fail) o
        # acceder a campos con relaciones y no solo al id
        export.append([
            result.fechaConsulta, result.videoId, result.fechaPublicacion, result.comentario, result.trend,
            result.comentarioLikes,
            result.comentarioRespuestas, result.isTopLevel
        ])
    # se transforma el array a una hoja de calculo en memoria
    sheet = excel.pe.Sheet(export)
    # se devuelve como "Response" el archivo para que se pueda "guardar"
    # en el navegador, es decir como hacer un "Download"
    return excel.make_response(sheet, "csv", file_name='youtube_comments_data' + (
        datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")) + '.csv')


# PARA LOS COMENTARIOS
def get_comment_threads(youtube, video_id, nextPageToken):
    if nextPageToken != None:
        results = youtube.commentThreads().list(
            part="snippet,replies",
            maxResults=100000,
            videoId=video_id,
            pageToken=nextPageToken,
            # searchTerms="textil", # se puede tambien filtrar por terminos de busqueda
            textFormat="plainText"
        ).execute()
    else:
        results = youtube.commentThreads().list(
            part="snippet,replies",
            maxResults=100000,
            videoId=video_id,
            textFormat="plainText"
        ).execute()
    if 'nextPageToken' in results:
        return results, True
    else:
        return results, False


def load_comments(match, fecha_consulta):
    # create a CSV output for video list

    for search_result in match.get("items", []):
        # print(search_result)
        # primero guardamos el comentario de mas alto nivel(padre)
        trend = search_result['id']
        videoId = search_result['snippet']['videoId']
        comment = search_result['snippet']['topLevelComment']['snippet']['textDisplay']
        commentLikeCount = search_result['snippet']['topLevelComment']['snippet']['likeCount']
        date = search_result['snippet']['topLevelComment']['snippet']['publishedAt']
        totalReplyCount = search_result['snippet']['totalReplyCount']
        isTopLevel = True
        comentarios = YoutubeComentario(videoId=videoId, fechaConsulta=fecha_consulta, fechaPublicacion=date,
                                        trend=trend, comentario=comment, comentarioLikes=commentLikeCount,
                                        comentarioRespuestas=totalReplyCount, isTopLevel=isTopLevel)
        comentarios.save()
        # comprobamos si el comentario tiene respuestas, en el caso de que tenga, las guardamos
        if 'replies' in search_result:
            # Tiene respuestas, guardamos los datos de esa respuesta
            replies = search_result['replies']
            for reply in search_result['replies']['comments']:
                comment = reply['snippet']['textDisplay']
                commentLikeCount = reply['snippet']['likeCount']
                date = reply['snippet']['publishedAt']
                totalReplyCount = 0
                isTopLevel = False
                comentarios = YoutubeComentario(videoId=videoId, fechaConsulta=fecha_consulta, fechaPublicacion=date,
                                                trend=trend, comentario=comment, comentarioLikes=commentLikeCount,
                                                comentarioRespuestas=totalReplyCount, isTopLevel=isTopLevel)
                comentarios.save()


# para las paginas
def video_comments(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_DEVELOPER_KEY)
    # abrimos la primera pagina de respuesta y comprobamos si tiene mas paginas
    print(video_id)
    match = get_comment_threads(youtube, video_id, None)
    fecha_consulta = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    # match[1] = boolean que indica si la respuesta tiene mas paginas
    # match[0] = resultado de la consulta
    hasPages = match[1]
    if hasPages:
        # si tiene paginas
        # obtenemos el token de la siguiente pagina
        next_page_token = match[0]["nextPageToken"]
        # guardamos los datos de la primera pagina
        load_comments(match[0], fecha_consulta)
        i = 1
        # mientras exista una siguiente pagina
        while next_page_token:
            # obtenemos los datos de la siguiente pagina pasando el token
            new_match = get_comment_threads(youtube, video_id, next_page_token)
            # guardamos el token de la siguiente pagina
            if new_match[1]:
                next_page_token = new_match[0]["nextPageToken"]
                # guardamos los datos de la pagina
                load_comments(new_match[0], fecha_consulta)
                print("\nPagina : ", i)
                print("------------------------------------------------------------------")
                i += 1
            else:
                load_comments(new_match[0], fecha_consulta)
                print("\nPagina : ", i)
                print("------------------------------------------------------------------")
                i += 1
                break
    else:
        # si la respuesta tiene una sola pagina, guardamos sus datos
        load_comments(match[0], fecha_consulta)
        print("Solo existe una pagina")


def youtube_search(query, region, publishedAfter):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_DEVELOPER_KEY)
    search_response = youtube.search().list(q=query, part="id,snippet", regionCode=region,
                                            publishedAfter=publishedAfter).execute()
    fecha_consulta = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            # videos.append("%s (%s)" % (search_result["snippet"]["title"],search_result["id"]["videoId"]))
            title = search_result["snippet"]["title"]
            title = unidecode.unidecode(title)  # Dongho 08/10/16
            videoId = search_result["id"]["videoId"]
            date = search_result["snippet"]["publishedAt"]
            video_response = youtube.videos().list(id=videoId, part="statistics").execute()
            for video_result in video_response.get("items", []):
                viewCount = video_result["statistics"]["viewCount"]

                if 'likeCount' not in video_result["statistics"]:
                    likeCount = 0
                else:
                    likeCount = video_result["statistics"]["likeCount"]
                if 'dislikeCount' not in video_result["statistics"]:
                    dislikeCount = 0
                else:
                    dislikeCount = video_result["statistics"]["dislikeCount"]
                if 'commentCount' not in video_result["statistics"]:
                    commentCount = 0
                else:
                    commentCount = video_result["statistics"]["commentCount"]
                # guardar los datos
                video = YoutubeVideo.objects.filter(videoId=videoId)
                print(len(video))
                if len(video) == 0:
                    # si no existe le guardo en la base
                    youtubeVideos = YoutubeVideo(videoId=videoId, titulo=title, fechaConsulta=fecha_consulta,
                                                 fechaPublicacion=date, numeroVistas=viewCount, numeroLikes=likeCount,
                                                 numeroDisLikes=dislikeCount, numeroComentarios=commentCount)
                    youtubeVideos.save()

                    # guardo todos los comentarios del video
                    video_comments(videoId)


class YoutubeParametros(View):
    def get(self, *args, **kwargs):
        formVideo = YoutubeVideoForm()
        formComentarios = YoutubeCommentForm()
        context = {
            'formVideo': formVideo,
            'formComentarios': formComentarios,
        }
        return render(self.request, "youtube/base.html", context)

    def post(self, *args, **kwargs):
        if 'videos' in self.request.POST:
            videosForm = YoutubeVideoForm(self.request.POST or None)
            if videosForm.is_valid():
                query = videosForm.cleaned_data.get('palabrasClave').split(', ')

                fecha = str(videosForm.cleaned_data.get('fecha')).split()[0] + 'T00:00:00Z'
                region = videosForm.cleaned_data.get('region')
                # hacemos la consulta y guardamos los datos
                try:
                    youtube_search(query, region, fecha)
                    for i in query:
                        # comparacion de si exite algun temino solo actualiza el numero de consulta
                        if TerminoBusqueda.objects.filter(nombre=i).exists():
                            datos = TerminoBusqueda.objects.filter(nombre=i)
                            TerminoBusqueda.objects.filter(nombre=i).update(
                                numero_consulta=datos[0].numero_consulta + 1)
                        else:
                            terminos_busqueda = TerminoBusqueda(
                                nombre=i, numero_consulta=1)
                            terminos_busqueda.save()
                    return redirect('app:pages:youtube_resultados')
                except:
                    messages.info(self.request,
                                  "Error al extraer los datos, revise que los parámetros son los correctos")
                    return redirect('app:pages:youtube')
            else:
                messages.info(self.request, "Error al procesar los parámetros de la solicitud")
                return redirect('app:pages:youtube')
        elif 'comentarios' in self.request.POST:
            comentariosForm = YoutubeCommentForm(self.request.POST or None)
            if comentariosForm.is_valid():
                return redirect('app:pages:youtube_resultados_comentarios')
            else:
                messages.info(self.request, "Error al procesar los parámetros de la solicitud")
                return redirect('app:pages:youtube')
                # messages.info(self.request, "Error al procesar los parámetros de la solicitud")
                # return redirect('app:pages:youtube')


class YoutubeVideoView(View):
    def get(self, *args, **kwargs):
        # obtenemos los datos de videos
        datosVideos = YoutubeVideo.objects.filter().order_by('-fechaConsulta')
        numeroDatos = len(datosVideos)
        page = self.request.GET.get('page', 1)
        paginator = Paginator(datosVideos, 10)
        try:
            videos = paginator.page(page)
        except PageNotAnInteger:
            videos = paginator.page(1)
        except EmptyPage:
            videos = paginator.page(paginator.num_pages)
        return render(self.request, "youtube/resultadosVideos.html", {
            'datosVideos': datosVideos,
            'numeroDatos': numeroDatos,
        })


class YoutubeComentariosView(View):
    def get(self, *args, **kwargs):
        # obtenemos los datos de comentarios
        datosComentarios = YoutubeComentario.objects.filter().order_by('-fechaConsulta')
        numeroDatos = len(datosComentarios)
        page = self.request.GET.get('page', 1)
        paginator = Paginator(datosComentarios, 10)
        try:
            comentarios = paginator.page(page)
        except PageNotAnInteger:
            comentarios = paginator.page(1)
        except EmptyPage:
            comentarios = paginator.page(paginator.num_pages)
        return render(self.request, "youtube/resultadosComentarios.html", {
            'datosComentarios': datosComentarios,
            'numeroDatos': numeroDatos,

        })
