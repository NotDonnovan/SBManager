from django.shortcuts import render
import qbittorrentapi
import environ
from .functions import status_rename
from hurry.filesize import size, alternative


env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env()

qbt_client = qbittorrentapi.Client(
    host=env('qbt_host'),
    port=8080,
    username=env('qbt_user'),
    password=env('qbt_password'))

torrents = [{'name': torrent.name,
             'state': status_rename(torrent.state),
             'progress': (torrent.progress * 100),
             'size': (size(torrent.size, system=alternative)),
             'ratio': (round(torrent.ratio, 2)),
             }
            for torrent in qbt_client.torrents_info()]


def home(request):
    return render(request, 'application/index.html', {'torrents': torrents})

def client_settings(request):
    return render(request, 'application/client_settings.html')

def new_client(request):
    pass