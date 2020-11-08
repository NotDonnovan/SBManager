from application.models import Seedbox
import subprocess


def remote_to_local(source, destination):
    file = f'{source.save_loc}'
    usr = 'pi'
    password = source.password
    host = source.host

    cmd = subprocess.Popen(f"sshpass -p {password} scp -T {usr}@{host}:{file} {destination}", stdout=subprocess.PIPE, shell=True)

    out, err = cmd.communicate()
    print(f"{file}")
    print(out.decode())

