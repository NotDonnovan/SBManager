from django import forms
from django.forms.formsets import BaseFormSet

class NewClient(forms.Form):
    name = forms.CharField(max_length=20)
    host = forms.GenericIPAddressField()
    login = forms.CharField(max_length=100,initial='admin')
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    port = forms.FloatField(initial=8080)

class CatForm(forms.Form):
    name = forms.CharField(max_length=100, label='Category', required=False)
    path = forms.CharField(max_length=100, label='Path', required=False)

class CatFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        categories = []
        paths = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                category = form.cleaned_data['name']
                path = form.cleaned_data['path']

                if category and path:
                    if category in categories:
                        duplicates = True
                    categories.append(category)
                    paths.append(path)



                if duplicates:
                    raise forms.ValidationError(
                        'Categories cannot have duplicate names',
                        code='duplicates'
                    )

        return self.cleaned_data