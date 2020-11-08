from application.models import Seedbox
import subprocess



def remote_to_local(source, destination):
    cmd = subprocess.Popen("", stdout=subprocess.PIPE, shell=True)
    out, err = cmd.communicate()
    print(out.decode())
    print(err)


