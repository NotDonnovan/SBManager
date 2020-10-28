from django.shortcuts import render, redirect
from .functions import get_torrents
from .forms import NewClient, CatForm, CatFormSet
from .models import Seedbox, Category
from django.views.generic.list import ListView
from django.forms.formsets import formset_factory

torrents = get_torrents()

def home(request):
    return render(request, 'application/index.html', {'torrents': torrents})

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
            client = Seedbox(name=n, host=h, login=l, password=p, port=pt)
            client.save()
            return redirect("client_settings")
    else:
        form = NewClient()
    return render(request,'application/new_client.html', {'form': form})

def category_settings(request):
    FormSet = formset_factory(CatForm, formset=CatFormSet)
    new_cats = []



    if request.method == "POST":
        form = FormSet(request.POST)

        if form.is_valid():
            for cat in form:
                category = cat.cleaned_data.get('category')
                new_cats.append(Category(name=category))

            try:
                with transaction.atomic():
                    Category.objects.bulk_create(new_cats)
                    return redirect("home", store=store)

            except IntegrityError:
                messages.error(request, 'Error')

    else:
        form = FormSet()
    return render(request, 'application/categories.html', {'form': form})