from django.shortcuts import render
from django.views import generic
from django.views.generic import View
from .forms import YoutubeVideoForm, YoutubeCommentForm
from .models import YoutubeVideo
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

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
                return redirect('app:pages:youtube_resultados')
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

class YoutubeVideo(View):
    def get(self, *args, **kwargs):
        return render(self.request, "youtube/resultadosVideos.html")


class YoutubeComentarios(View):
    def get(self, *args, **kwargs):
        return render(self.request, "youtube/resultadosComentarios.html")