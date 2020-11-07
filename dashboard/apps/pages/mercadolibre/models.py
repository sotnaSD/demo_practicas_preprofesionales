
from django.db import models

# Modelo de la tabla para la plataforma mercado libre
class MercadoLibre(models.Model):
    consulted_at = models.DateTimeField(auto_now=True)
    nombre = models.CharField(max_length=300,primary_key=True)
    url = models.CharField(max_length=300,default=None)
    def __str__(self):
        return self.nombre