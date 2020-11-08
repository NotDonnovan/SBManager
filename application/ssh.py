import subprocess
from .models import Seedbox


cmd = subprocess.Popen("ls" , stdout=subprocess.PIPE, shell=True)
out, err = cmd.communicate()

print(out.decode())