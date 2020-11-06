from django import forms
from .functions import get_directories
from django.forms.formsets import BaseFormSet

path_choices = get_directories()

class NewClient(forms.Form):
    name = forms.CharField(max_length=20)
    host = forms.GenericIPAddressField()
    login = forms.CharField(max_length=100,initial='admin')
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    port = forms.FloatField(initial=8080)

class NewDevice(forms.Form):
    name = forms.CharField(max_length=20)
    host = forms.GenericIPAddressField()


class DirForm(forms.Form):
    path_name = forms.CharField(max_length=20, label='Path Name', required=False)
    path = forms.CharField(max_length=200, label='Path',initial='/', required=False)

class DirFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        names = []
        paths = []
        duplicate_name = False
        duplicate_path = False

        for form in self.forms:
            if form.cleaned_data:
                path_name = form.cleaned_data['path_name']
                path = form.cleaned_data['path']

                if path_name and path:
                    if path_name in names:
                        duplicate_name = True
                    if path in paths:
                        duplicate_path = True
                    names.append(path_name)
                    paths.append(path)



                if duplicate_name:
                    raise forms.ValidationError(
                        'Path names must be different',
                        code='duplicates'
                    )

                if duplicate_path:
                    raise forms.ValidationError(
                        'Paths must be different',
                        code='duplicates'
                    )

        return self.cleaned_data

class CatForm(forms.Form):
    name = forms.CharField(max_length=100, label='Category', required=False)
    path = forms.CharField(max_length=100, label='Path', required=False, widget=forms.Select(choices=path_choices))

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

                if category:
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