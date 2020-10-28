from .models import Seedbox
import qbittorrentapi
from hurry.filesize import size, alternative

def status_rename(string):
    status = {
        'pausedUP' : 'Complete',
        'stalledUP' : 'Seeding (Idle)',
        'uploading' : 'Seeding',
        'forcedUP': 'Seeding (f)',
        'queuedUP' : 'Queued',
        'queuedDL' : 'Queued',
        'checkingUP' : 'Checking',
        'downloading' : 'Downloading',
        'forceDL' : 'Downloading (f)',
        'metaDL' : 'Fetching Metadata',
        'pausedDL' : 'Paused',
        'stalledDL' : 'Stalled',
        'checkingDL' : 'Checking',
        'checkingResumeData' : 'Checking',
    }

    if string in status.keys():
        string = status[string]

    return string

def get_torrents():
    clients = []
    torrents = []

    for box in Seedbox.objects.all():
        clients.append({
            box.name : qbittorrentapi.Client(
                host=box.host,
                port=box.port,
                username=box.login,
                password=box.password)
        }
        )

    for client in range(len(clients)):
        for obj in clients[client].values():
            for torrent in obj.torrents_info():
                torrents.append(
                    {'name': torrent.name,
                     'state': status_rename(torrent.state),
                     'progress': (torrent.progress * 100),
                     'size': (size(torrent.size, system=alternative)),
                     'ratio': (round(torrent.ratio, 2)),
                     'client': list(clients[client].keys())[0]
                     }
                )
    return torrents

def pull_categories(client):
    qbt_client = qbittorrentapi.Client(
        host=client.host,
        port=client.port,
        username=client.login,
        password=client.password
    )



