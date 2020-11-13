import subprocess
from time import sleep

def remote_to_local(source, destination):
    file = f'{source.save_loc}'
    usr = 'pi'
    password = source.password
    host = source.host

    cmd = subprocess.Popen(f"sshpass -p {password} scp -T {usr}@{host}:{file} {destination}", stdout=subprocess.PIPE,
                           shell=True)

    out, err = cmd.communicate()
    print(f"{file}")
    print(out.decode())


def remote_to_remote(source, destination):
    from application.models import MoveQueue

    print('MOVING')
    sleep(15)
    #cmd = subprocess.Popen(
    #    f"scp -r -p {source['client'].user}@{source['client'].host}:{source['client'].save_loc}{source['file']} "
    #    f"{destination['device'].user}@{destination['device'].host}:{destination['folder']}", shell=True)

    #out, err = cmd.communicate()
    #print(out.decode())

    q = MoveQueue.objects.get(torrent=source['torrent'])
    q.status = 'moved'
    q.save()

    print('DONE')
