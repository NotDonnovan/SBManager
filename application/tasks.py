from time import sleep
from .functions import get_torrents
from .models import MoveQueue, Category, Directory, Moving, Moved
from .transfer.ssh import remote_to_local, remote_to_remote
from .models import Seedbox

def check_finished_download():
    while True:
        categories = Category.objects.all()
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
    queue = MoveQueue.objects.all()
    moving = Moving.objects.all().values_list('filename', flat=True)
    moved = Moved.objects.all().values_list('filename', flat=True)

    for file in queue:
        #print(f'{file.filename} will be moved to {file.category.device.name}s {file.category.name} folder which is {Directory.objects.get(label=file.category.name).path}')
        source = {'client': file.client,
                  'file': file.filename}

        destination = {'device': file.category.device,
                       'folder': Directory.objects.get(label=file.category.name).path}

        if file.category.device.type == 'ssh':
            if file.filename not in moving or file.filename not in moved:
                m = Moving(filename=file.filename)
                m.save()
                print('MOVING1')
                remote_to_remote(source=source, destination=destination)
