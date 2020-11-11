import subprocess


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
    from application.models import Moved, Moving

    print('MOVING')

    cmd = subprocess.Popen(
        f"scp -r -p {source['client'].user}@{source['client'].host}:{source['client'].save_loc}{source['file']} "
        f"{destination['device'].user}@{destination['device'].host}:{destination['folder']}", shell=True)

    out, err = cmd.communicate()
    print(out.decode())
    m = Moved(filename=source['file'])
    m.save()
    Moving.objects.get(filename=source['file']).delete()
    print('DONE')
