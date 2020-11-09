from time import sleep
from .functions import get_torrents
from .models import MoveQueue, Category, Directory

categories = Category.objects.all()


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
                        new_files.append(MoveQueue(filename=name, category=cat))

        MoveQueue.objects.bulk_create(new_files)

        if MoveQueue.objects.all():
            move_downloads()
        sleep(60)


def move_downloads():
    paths = Directory.objects.all()
    queue = MoveQueue.objects.all()

    for c in categories:
        for file in queue:
            if file.category == c.name:
                for p in paths:
                    if c.device == p.device:
                        print(f'{file.filename} will be moved to {c.path.split(" | ")[1]}s {c.name} folder')
    for dl in MoveQueue.objects.all():
        pass
