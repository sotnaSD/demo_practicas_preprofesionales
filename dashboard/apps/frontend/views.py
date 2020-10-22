from django.shortcuts import render
from django.views import generic


# Create your views here.
class IndexView(generic.TemplateView):
    """
    IndexView:
    """
    module = 'indexView'
    template_name = 'frontend/base.html'

    