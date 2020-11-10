from time import sleep
from .functions import get_torrents
from .models import MoveQueue, Category, Directory
from .transfer.ssh import remote_to_local
categories = Category.objects.all()
from .models import Seedbox

def check_finished_download():
    while True:
        new_files = []
        torrents = get_torrents()
        queue = MoveQueue.objects.all().values_list('filename', flat=True)
        for t in torrents:
            cat, name, prog = t['category'], t['name'], t['progress']
            if prog == 100 and name not in queue:
                for c in categories:
                    if c.name == cat and c.path != 'None':
                        new_files.append(MoveQueue(filename=name, category=Category.objects.get(name=cat), client=Seedbox.objects.get(name=t['client'])))

        MoveQueue.objects.bulk_create(new_files)

        if MoveQueue.objects.all():
            move_downloads()
        sleep(60)


def move_downloads():
    paths = Directory.objects.all()
    queue = MoveQueue.objects.all()

    for file in queue:
        print(f'{file.filename} will be moved to {file.category.path.split(" | ")[1]}s {file.category.name} folder')
