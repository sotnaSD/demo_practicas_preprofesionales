from django import forms

class YoutubeVideoForm(forms.Form):
    palabrasClave = forms.CharField(required=True)
    fecha = forms.DateTimeField(required=True)
    region = forms.CharField(required=True)

class YoutubeCommentForm(forms.Form):
    videoId = forms.CharField(required=True)