from django.shortcuts import render
import qbittorrentapi
import environ
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


def home(request):

    torrents = [{'tname': torrent.name, 'tstate': torrent.state}
                 for torrent in qbt_client.torrents_info()]

    return render(request, 'application/index.html', {'torrents': torrents})