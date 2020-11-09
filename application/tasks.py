from time import sleep
from .functions import get_torrents
from .models import MoveQueue, Category


def check_finished_download():
    while True:
        new_files = []
        torrents = get_torrents()
        queue = MoveQueue.objects.all().values_list('filename', flat=True)

        for t in torrents:
            cat, name, prog = t['category'], t['name'], t['progress']
            categories = Category.objects.all()
            if prog == 100 and name not in queue:
                for c in categories:
                    if c.name == cat and c.path != 'None':
                        new_files.append(MoveQueue(filename=name, category=cat))

        MoveQueue.objects.bulk_create(new_files)

        if MoveQueue.objects.all():
            move_downloads()
        sleep(60)

def move_downloads():
    for dl in MoveQueue.objects.all():
        print(dl.filename)