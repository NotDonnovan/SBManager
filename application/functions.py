import qbittorrentapi
from hurry.filesize import size, alternative

from .models import Seedbox, Category, Directory, Device, Torrent


def status_rename(string):
    status = {
        'pausedUP': 'Complete',
        'stalledUP': 'Seeding (Idle)',
        'uploading': 'Seeding',
        'forcedUP': 'Seeding (f)',
        'queuedUP': 'Queued',
        'queuedDL': 'Queued',
        'checkingUP': 'Checking',
        'downloading': 'Downloading',
        'forceDL': 'Downloading (f)',
        'metaDL': 'Fetching Metadata',
        'pausedDL': 'Paused',
        'stalledDL': 'Stalled',
        'checkingDL': 'Checking',
        'checkingResumeData': 'Checking',
    }

    if string in status.keys():
        string = status[string]

    return string


def get_torrents():
    clients = []
    torrents = []
    tors_in_client = []
    old_torrents = Torrent.objects.all().values_list('name', flat=True)

    for box in Seedbox.objects.all():
        clients.append({
            box.name: qbittorrentapi.Client(
                host=box.host,
                port=box.port,
                username=box.login,
                password=box.password)
        }
        )

    for client in range(len(clients)):
        for obj in clients[client].values():
            for torrent in obj.torrents_info(sort='progress', reverse=True):
                new_torrent = Torrent(name=torrent.name,
                                      state=status_rename(torrent.state),
                                      progress=(round(torrent.progress * 100)),
                                      size=(size(torrent.size, system=alternative)),
                                      ratio=(round(torrent.ratio, 2)),
                                      client=Seedbox.objects.get(name=list(clients[client].keys())[0]),
                                      category=Category.objects.get(name=torrent.category)
                                      )
                tors_in_client.append(new_torrent)

                if torrent.name not in old_torrents:
                    torrents.append(new_torrent)

    if Torrent.objects.exists():
        names = []
        for t in tors_in_client:
            names.append(t.name)

        for o in old_torrents:
            if o in names:
                print(f'Not Deleting {o}')
            else:
                print(f'Deleting {o}')
                Torrent.objects.get(name=o).delete()

    Torrent.objects.bulk_create(torrents)


def pull_categories(client):
    qbt_client = qbittorrentapi.Client(
        host=client.host,
        port=client.port,
        username=client.login,
        password=client.password
    )
    categories = list(Category.objects.all().values_list('name', flat=True))
    client_categories = list(qbt_client.torrents_categories())
    new_categories = []

    for category in client_categories:
        if category in categories:
            pass
        else:
            new_categories.append(Category(name=category))

    if new_categories:
        print('adding new cats')
        Category.objects.bulk_create(new_categories)


def get_directories():
    dirs = [('None', 'None')]
    d = []
    used = {}
    for dev in list(Directory.objects.all().values_list('device', flat=True)):
        devname = Device.objects.get(pk=dev).name
        for dirname in list(Directory.objects.all().values_list('label', flat=True)):
            if devname in list(used.keys()):
                pass
            else:
                used[devname] = []

            if dirname in Directory.objects.filter(device=dev).values_list('label', flat=True):
                if dirname in used[devname]:
                    pass
                else:
                    used[devname].append(dirname)
                    d.append(f'{dirname} | {devname}')
                    d.append('{} | {}'.format(devname, dirname))
                    d = tuple(d)
                    dirs.append(d)
                    d = []

    return dirs


def get_save_location(client):
    qbt_client = qbittorrentapi.Client(
        host=client.host,
        port=client.port,
        username=client.login,
        password=client.password
    )
    return (qbt_client.app.defaultSavePath)


def ping(ip):
    import subprocess
    from time import sleep
    cmd = subprocess.Popen(f'if ping -c 1 {ip} &> /dev/null; then echo PASS; else echo "FAIL"; fi',stdout=subprocess.PIPE, shell=True)

    out, err = cmd.communicate()
    print(out)
    print(err)
