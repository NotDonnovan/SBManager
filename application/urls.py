from django.urls import path
from . import views
from .tasks import check_finished_download
import threading

urlpatterns = [
    path('', views.home, name='index'),
    path('settings/clients', views.ClientSettings.as_view(), name='client_settings'),
    path('settings/add_client', views.new_client, name='new_client'),
    path('settings/clients/edit/<int:pk>', views.EditClient.as_view(), name='edit_client'),
    path('settings/clients/delete/<int:pk>', views.DelClient.as_view(), name='delete_client'),
    path('settings/devices', views.DeviceSettings.as_view(), name='devices'),
    path('settings/add_device', views.new_device, name='new_device'),
    path('settings/devices/edit/<int:pk>', views.EditDevice.as_view(), name='edit_device'),
    path('settings/devices/delete/<int:pk>', views.DelDevice.as_view(), name='delete_device'),
    path('settings/categories', views.category_settings, name='categories'),


]
#check_finished_download()
b = threading.Thread(name='Check downloads', target=check_finished_download)
b.start()