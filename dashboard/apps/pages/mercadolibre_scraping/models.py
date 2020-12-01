from django.db import models


# Create your models here.
class ProductoMercadoLibre(models.Model):
    """
    Modelo para guardar datos de  mercado libre
    """
    id_busqueda = models.IntegerField()
    id_producto = models.IntegerField()
    titulo = models.CharField(max_length=200)
    precio = models.CharField(max_length=30)
    ubicacion = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    url = models.CharField(max_length=200)

