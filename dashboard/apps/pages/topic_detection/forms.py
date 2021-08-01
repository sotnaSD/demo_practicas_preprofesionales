from django import forms


class TopicDetectionForm(forms.Form):
    model = forms.CharField(required=True)
    n_clusters = forms.CharField(required=True)
    

    # def clean(self):
    #     cleaned_data = super().clean()
    #     input_pais = cleaned_data.get('input_pais')
    #     input_categoria = cleaned_data.get('input_categoria')

    #     if input_pais == 'Seleccione un Pais':
    #         msg = "Seleccion un pais"
    #         self.add_error('input_pais', msg)
    #     elif input_categoria == 'Seleccione una categoria':
    #         msg = "Seleccione un categoria"
    #         self.add_error('input_categoria', msg)
