from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import generic
# importacion del forms de la app mercado libre
from .forms import MercadoLibreForm
# importacion de metodos que se conectan con la api de mercado libre
from .utils import getPaisMercadoLibre
from .utils import getCategoryMercadoLibre
from .utils import getTrendsMercadoLibre
# importacion de modelos
from .models import MercadoLibre
from ...frontend.models import TerminoBusqueda
from ..mercadolibre_scraping.utils import start_crawler
# importacion de modulos
from datetime import datetime
import django_excel as excel
import time


# Vista para la app frontend
class IndexView(generic.View):
    """
    IndexView: clase principal para la plataforma de mercado libre tendencias
    """

    # metodo get para IndexView de mercado libre
    def get(self, *args, **kwargs):
        datos = MercadoLibre.objects.all()
        name_columns = MercadoLibre._meta.fields
        # parametros para el template tabla.html
        context = {
            'num_registros': datos.count(),
            'num_parametros': len(name_columns),
            'paises': getPaisMercadoLibre()
        }
        # return template con paises
        return render(self.request, 'mercadolibre/base.html', context)

    # metodo pos para IndexView de mercado libre
    def post(self, *args, **kwargs):
        # condicional para el ajax del combo box
        if 'action' in list(self.request.POST.keys()):
            data = getCategoryMercadoLibre(self.request.POST['id'])
            return JsonResponse(data, safe=False)

        # Guardar datos y termino de la busqueda
        formMercadoLibre = MercadoLibreForm(self.request.POST or None)
        if formMercadoLibre.is_valid():

            # Guardar datos obtenenidos en la base de datos
            id_pais = formMercadoLibre.cleaned_data['input_pais'].split('-')
            id_categoria = formMercadoLibre.cleaned_data['input_categoria'].split('-')
            datos = getTrendsMercadoLibre(id_pais[0], id_categoria[0])
            try:
                for data in datos.json():
                    mercado_libre = MercadoLibre(
                        nombre=data['keyword'], url=data['url'])
                    mercado_libre.save()
            except Exception as e:
                print(e)

            # Guardar termino de busqueda
            txt_busqueda = str(id_pais[1] + '-' + id_categoria[1])
            if TerminoBusqueda.objects.filter(nombre=txt_busqueda).exists():
                datos = TerminoBusqueda.objects.filter(nombre=txt_busqueda)
                TerminoBusqueda.objects.filter(nombre=txt_busqueda).update(numero_consulta=datos[0].numero_consulta + 1)
            else:
                terminos_busqueda = TerminoBusqueda(nombre=txt_busqueda, numero_consulta=1)
                terminos_busqueda.save()
            return redirect('app:pages:mercadolibre_resultados')
        else:
            context = {
                'formMercadoLibre': formMercadoLibre,
                'paises': getPaisMercadoLibre(),
            }
            return render(self.request, 'mercadolibre/base.html', context)


class MercadoLibreResutlados(generic.View):
    """
    Clase para mostrar la pagina de los resultados de mercado libre tendencias
    """
    # metodo get del MercadoLibre resultado de mercado libre
    # Muestra los resultados en una tabla
    def get(self, *args, **kwargs):
        # consulta a la base de datos
        datos = MercadoLibre.objects.all()
        name_columns = MercadoLibre._meta.fields
        # parametros para el template tabla.html
        context = {
            'num_registros': datos.count(),
            'num_parametros': len(name_columns),
            'datos': datos,
            'name_columns': name_columns
        }
        return render(self.request, 'mercadolibre/tabla.html', context)

    def post(self, *args, **kwargs):
        # condicion para que si es un ajax ingrese y haga scraping al enlace
        if 'url' in self.request.POST.keys():
            import time
            # time.sleep(1)
            try:
                # obtencion de la url y separacion de la palabra de busqueda
                query = self.request.POST['url'].split('/')[-1]
                # llamar al metodo start_crawler de utils de la aplicacion mercadolibre_scraping
                start_crawler(query, '2')
                # time
                time.sleep(1)
                # return un json de confirmacion que se realizo el crawler.
                return JsonResponse({'respuesta': 'Se ha realizado el crawler de ' + query})
            except Exception as e:
                # retornas un respuesta cuando ocurra un error.
                return JsonResponse({'error': 'Ocurrio un error: ' + e})

        # exportar datos como csv\
        if self.request.method == "POST":
            export = []
            # Se agregan los encabezados de las columnas
            export.append([
                'consulted_at',
                'nombre',
                'url'])

            # Se obtienen los datos de la tabla o model y se agregan al array
            results = MercadoLibre.objects.all()
            for result in results:
                # agregar las filas 
                export.append([
                    result.consulted_at,
                    result.nombre,
                    result.url])

            # Obtenemos la fecha para agregarla al nombre del archivo
            today = datetime.now()
            strToday = today.strftime("%Y%m%d")

            # se transforma el array a una hoja de calculo en memoria
            sheet = excel.pe.Sheet(export)

            # se devuelve como "Response" el archivo para que se pueda "guardar"
            # en el navegador, es decir como hacer un "Download"
            return excel.make_response(sheet, "csv", file_name="mercadolibre-tendencias-" + strToday + ".csv")
