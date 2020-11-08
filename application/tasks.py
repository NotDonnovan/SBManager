from time import sleep
from .functions import get_torrents
from .models import MoveQueue


def check_finished_download():
    while True:
        new_files = []
        torrents = get_torrents()
        queue = MoveQueue.objects.all.values_list('filename', flat=True)

        for t in torrents:
            cat, name, state = t['category'], t['name'], t['state']
            if state == 'Complete':
                if name not in queue:
                    new_files.append(MoveQueue(filename=name, category=cat))



        sleep(30)
