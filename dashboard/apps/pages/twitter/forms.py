import datetime

import tweepy
from django import forms
from django.conf import settings

# from django.utils.datetime_safe import datetime
class TwitterForm(forms.Form):
    input_fecha_inicio = forms.DateField(required=True, )
    input_fecha_fin = forms.DateField(required=False)
    input_palabras_claves = forms.CharField(required=True)
    input_ubicacion = forms.CharField(required=False)
    input_idioma= forms.CharField(required=True)
    
    def clean_input_palabras_claves(self):
        input_palabras_claves = self.cleaned_data['input_palabras_claves'].strip()
        # do some other validation if you want...
        return input_palabras_claves

    def clean_input_ubicacion(self):
        input_ubicacion = self.cleaned_data['input_ubicacion'].strip()
        # do some other validation if you want...
        return input_ubicacion 


    def clean(self):
        cleaned_data = super().clean()
        input_fecha_inicio = cleaned_data.get('input_fecha_inicio')
        input_fecha_fin = cleaned_data.get('input_fecha_fin')
        if input_fecha_inicio != None and input_fecha_fin != None:
            if input_fecha_inicio > datetime.date.today():
                msg = "La fecha no puede ser  mayor a la de hoy"
                self.add_error('input_fecha_inicio', msg)
            elif input_fecha_fin > datetime.date.today():
                msg = "La fecha no puede ser  mayor a la de hoy"
                self.add_error('input_fecha_fin', msg)

            elif input_fecha_inicio == input_fecha_fin:
                msg = "No pueden ser fechas iguales"
                self.add_error('input_fecha_inicio', msg)
                self.add_error('input_fecha_fin', msg)

            elif input_fecha_inicio > input_fecha_fin:
                msg = "Fecha inicio no puede ser mayor la fecha final."
                self.add_error('input_fecha_inicio', msg)
        