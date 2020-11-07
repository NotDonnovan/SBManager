from django.shortcuts import render, redirect
from .functions import get_torrents, pull_categories
from .forms import *
from .models import *
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.forms.formsets import formset_factory
from django.db import IntegrityError, transaction
from django.contrib import messages

def home(request):
    return render(request, 'application/index.html', {'torrents': get_torrents()})

class ClientSettings(ListView):
    model = Seedbox
    template_name = 'application/client_settings.html'

    def get_queryset(self):
        return Seedbox.objects.all()

def new_client(request):
    if request.method == "POST":
        form = NewClient(request.POST)
        if form.is_valid():
            n = form.cleaned_data['name']
            h = form.cleaned_data['host']
            l = form.cleaned_data['login']
            p = form.cleaned_data['password']
            pt = form.cleaned_data['port']
            client = Seedbox(name=n, host=h, login=l, password=p, port=int(pt))
            client.save()
            pull_categories(client)
            return redirect("client_settings")
    else:
        form = NewClient()
    return render(request,'application/new_client.html', {'form': form})

class EditClient(UpdateView):
    model = Seedbox
    form_class = EditClientForm
    template_name = 'application/new_client.html'

def new_device(request):
    FormSet = formset_factory(DirForm, formset=DirFormSet)
    new_dirs = []

    if request.method == "POST":
        form = NewDevice(request.POST)
        formset = FormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            n = form.cleaned_data['name']
            h = form.cleaned_data['host']
            d = Device(name=n, host=h)
            d.save()

            for dir in formset:
                path_name = dir.cleaned_data.get('path_name')
                path = dir.cleaned_data.get('path')

                if path_name and path:
                    new_dirs.append(Directory(device=d, label=path_name, path=path))

            try:
                with transaction.atomic():
                    Directory.objects.bulk_create(new_dirs)
                    return redirect("devices")

            except IntegrityError: #If the transaction failed
                messages.error(request, 'Error')
        print('formset errors: {}'.format(formset.errors))
        print('form errors: {}'.format(form.errors))
    else:
        form = NewDevice()
        formset = FormSet()
    return render(request,'application/new_device.html', {'form': form, 'formset': formset})

def category_settings(request):
    get_directories()
    FormSet = formset_factory(CatForm, formset=CatFormSet)
    current_cats = list(Category.objects.all())
    data = [{'name': c.name, 'path': c.path}
            for c in current_cats]
    new_cats = []

    if request.method == "POST":
        form = FormSet(request.POST)

        if form.is_valid():

            for cat in form:
                category = cat.cleaned_data.get('name')
                path = cat.cleaned_data.get('path')

                if category:
                    new_cats.append(Category(name=category, path=path))

            try:
                with transaction.atomic():
                    Category.objects.all().delete()
                    Category.objects.bulk_create(new_cats)
                    return redirect("categories")

            except IntegrityError:
                messages.error(request, 'Error')

    else:
        form = FormSet(initial=data)
    return render(request, 'application/categories.html', {'form': form})

class DeviceSettings(ListView):
    model = Device
    template_name = 'application/devices.html'

    def get_queryset(self):
        return Device.objects.all()