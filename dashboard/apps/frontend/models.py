from django.db import models

# Create your models here.
# Create your models here.
class TerminoBusqueda(models.Model):
    nombre = models.CharField( max_length=50, primary_key=True)
    numero_consulta = models.IntegerField()
    def __str__(self):
        return self.nombre
