from django import forms
from .functions import get_directories
from django.forms.formsets import BaseFormSet
from .models import Seedbox, Device

transfer_types = [
    ('Local', 'Local'),
    ('ssh', 'SSH'),
    ('smb', 'SMB'),
    ('ftp', 'FTP'),
]

class NewClient(forms.Form):
    name = forms.CharField(max_length=20)
    host = forms.GenericIPAddressField()
    login = forms.CharField(max_length=100,initial='admin')
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    port = forms.FloatField(initial=8080)
    user = forms.CharField(max_length=20, label='User (SSH)')
    save_loc = forms.CharField(max_length=200, initial='/', label='Save Location',
                               widget=forms.TextInput(attrs={'class': 'tooltipped',
                                                             'data-position': 'top',
                                                             'data-tooltip': 'Where does this client save its downloads?'}))


class EditClientForm(forms.ModelForm):
    save_loc = forms.CharField(max_length=200, initial='/',label='Save Location',
                               widget=forms.TextInput(attrs={'class': 'tooltipped',
                                                             'data-position': 'top',
                                                             'data-tooltip': 'Where does this client save its downloads?'}))
    class Meta:
        model = Seedbox

        fields = [
            'name',
            'host',
            'login',
            'password',
            'port',
            'save_loc',
            'user'
        ]
        widgets = {
            'password': forms.TextInput(attrs={'type': 'password'}),
        }

class NewDevice(forms.Form):

    name = forms.CharField(max_length=20)
    host = forms.GenericIPAddressField()
    #type = forms.CharField(max_length=100,label='Type', widget=forms.Select(choices=transfer_types), initial='ssh')
    user = forms.CharField(max_length=20)


class EditDeviceForm(forms.ModelForm):

    class Meta:
        model = Device

        fields = [
            'name',
            'host',
            'type',
            'user',
        ]
        widgets = {
            'type': forms.Select(choices=transfer_types),

        }

class DirForm(forms.Form):
    path_name = forms.CharField(max_length=20, label='Path Name', required=False)
    path = forms.CharField(max_length=200, label='Path', initial='/', required=False)

class DirFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        names = []
        paths = []
        duplicate_name = False

        for form in self.forms:
            if form.cleaned_data:
                path_name = form.cleaned_data['path_name']
                path = form.cleaned_data['path']

                if path_name and path:
                    if path_name in names:
                        duplicate_name = True
                    names.append(path_name)
                    paths.append(path)

                if duplicate_name:
                    raise forms.ValidationError(
                        'Path names must be different',
                        code='duplicates'
                    )


        return self.cleaned_data

class CatForm(forms.Form):
    name = forms.CharField(max_length=100, label='Category', required=False)
    path = forms.CharField(max_length=100, label='Path', required=False, widget=forms.Select(choices=get_directories()))

    def __init__(self, *args, **kwargs):
        super(CatForm, self).__init__(*args, **kwargs)
        self.fields['path'] = forms.ChoiceField(choices=get_directories())

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


