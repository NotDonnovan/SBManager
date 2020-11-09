
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.forms.formsets import formset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic.list import ListView
from django.core.management import call_command
from .forms import *
from .functions import get_torrents, pull_categories, get_save_location
from .models import *


def home(request):
    #remote_to_local(Seedbox.objects.get(pk=13),'/home/dpasc/testing')
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
            save_loc = get_save_location(client)
            client.save_loc = save_loc
            client.save()
            pull_categories(client)
            return redirect("client_settings")
    else:
        form = NewClient()
    return render(request,'application/new_client.html', {'form': form, 'can_delete': False})

class EditClient(UpdateView):
    model = Seedbox
    form_class = EditClientForm
    template_name = 'application/new_client.html'

    def get_success_url(self):
        return reverse_lazy("client_settings")

class DelClient(DeleteView):
    model = Seedbox
    def get_success_url(self):
        return reverse_lazy("client_settings")

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
    return render(request,'application/new_device.html', {'form': form, 'formset': formset, 'can_delete': False})

class EditDevice(UpdateView):
    model = Device
    form_class = EditDeviceForm
    FormSet = formset_factory(DirForm, formset=DirFormSet)
    template_name = 'application/new_device.html'

    def get_context_data(self, **kwargs):
        context = super(EditDevice, self).get_context_data(**kwargs)
        current_dirs = Directory.objects.filter(device=self.get_object())
        dir_data = [{'path_name': direc.label, 'path': direc.path}
                     for direc in current_dirs]
        context['formset'] = self.FormSet(initial=dir_data)
        return context

    def dispatch(self, request, *args, **kwargs):
        d = Device.objects.get(pk=self.get_object().id)
        if request.method == 'POST':
            formset = self.FormSet(request.POST)

            if formset.is_valid():

                new_dirs = []

                for form in formset:
                    path_name = form.cleaned_data.get('path_name')
                    path = form.cleaned_data.get('path')

                    if path_name and path:
                        new_dirs.append(Directory(device=d, label=path_name, path=path))
                try:
                    with transaction.atomic():
                        Directory.objects.filter(device=d).delete()
                        Directory.objects.bulk_create(new_dirs)

                except IntegrityError:  # If the transaction failed
                    messages.error(request, 'Error')

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("devices")

class DelDevice(DeleteView):
    model = Device
    def get_success_url(self):
        return reverse_lazy("devices")

def category_settings(request):

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
                path_dev = cat.cleaned_data.get('path')

                if path_dev != 'None':
                    device = path_dev.split(" | ")[1]

                if category and path_dev != 'None':
                    new_cats.append(Category(device=Device.objects.get(name=device), name=category, path=path_dev))
                if category and path_dev == 'None':
                    new_cats.append(Category(name=category, path=path_dev))

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