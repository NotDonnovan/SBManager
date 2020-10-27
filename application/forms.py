from django import forms

class NewClient(forms.Form):
    name = forms.CharField(max_length=20)
    host = forms.GenericIPAddressField()
    login = forms.CharField(max_length=100,initial='admin')
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    port = forms.FloatField(initial=8080)