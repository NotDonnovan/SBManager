from django.contrib import admin
from .models import Seedbox, Category, Device, MoveQueue

admin.site.register(Seedbox)
admin.site.register(Category)
admin.site.register(Device)
admin.site.register(MoveQueue)