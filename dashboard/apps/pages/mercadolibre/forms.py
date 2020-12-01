from django import forms
from django.conf import settings
import tweepy
import datetime


# from django.utils.datetime_safe import datetime
class MercadoLibreForm(forms.Form):
    input_pais = forms.CharField(required=True)
    input_categoria = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        input_pais = cleaned_data.get('input_pais')
        input_categoria = cleaned_data.get('input_categoria')

        if input_pais == 'Seleccione un Pais':
            msg = "Seleccion un pais"
            self.add_error('input_pais', msg)
        elif input_categoria == 'Seleccione una categoria':
            msg = "Seleccione un categoria"
            self.add_error('input_categoria', msg)
