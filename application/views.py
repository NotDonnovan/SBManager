from django.shortcuts import render, redirect
from .functions import status_rename, get_torrents
from .forms import NewClient
from .models import Seedbox
from django.views.generic.list import ListView

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
        print(form.errors)
    else:
        form = NewClient()
    return render(request,'application/new_client.html', {'form': form})