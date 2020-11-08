from background_task import background
import subprocess
from django.core.management import call_command
from time import sleep

class BackgroundTasks:
    def test_task():
        while 1:
            print('test')
            sleep(3)
