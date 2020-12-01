from django.db import models
from django.conf import settings


# Create your models here.
class ProductoPinterest(models.Model):
    """
    Modelo para guardar los datos de consultas de Pinterest con web scraping
    """
    fecha_consulta = models.DateTimeField(auto_now=True)
    titulo = models.CharField(max_length=200)
    url = models.CharField(max_length=200, primary_key=True)
    descripcion = models.CharField(max_length=201)
    url_imagen = models.CharField(max_length=50)


    #retorna todos los comentarios
    @property
    def get_comentario(self):
        return ProductoPinterestComentario.objects.filter(url=self.url)


class ProductoPinterestComentario(models.Model):
    url = models.ForeignKey('ProductoPinterest', on_delete=models.CASCADE);
    comentario = models.CharField(max_length=600, primary_key=True)
