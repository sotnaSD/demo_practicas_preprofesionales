from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'

class ExampleForms(forms.Form):
    my_data_field = forms.DateField(widget=DateInput)


class ExampleModelsForms(forms.Form):
    class Meta:
        widget={'my_data_field':DateInput()}
