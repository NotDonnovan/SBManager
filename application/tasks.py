from time import sleep
from .functions import get_torrents
from .models import MoveQueue, Category, Directory, Torrent
from .transfer.ssh import remote_to_local, remote_to_remote
from .models import Seedbox


def check_finished_download():
    moved = False
    while True:
        categories = Category.objects.all()
        new_files = []
        torrents = Torrent.objects.all()
        queue = MoveQueue.objects.all().values_list('torrent', flat=True)
        for t in torrents:
            if t.progress == 100 and t.id not in queue:
                for c in categories:
                    if c == t.category and c.path != 'None':
                        new_files.append(MoveQueue(torrent=t))

        MoveQueue.objects.bulk_create(new_files)

        if MoveQueue.objects.all():
            moved = move_downloads()
        if moved:
            sleep(60)


def move_downloads():
    queue = MoveQueue.objects.all()
    for file in queue:
        source = {'torrent': file.torrent,
                  'client': file.torrent.client,
                  'file': file.torrent.name}

        destination = {'device': file.torrent.category.device,
                       'folder': Directory.objects.get(label=file.torrent.category.name).path}

        if file.torrent.category.device.type == 'ssh' and file.status == 'queued':
            print('MOVING1')
            q = MoveQueue.objects.get(torrent=file.torrent)
            q.status = 'moving'
            q.save()
            remote_to_remote(source=source, destination=destination)
            return True

        if file.status != 'queued':
            return False
