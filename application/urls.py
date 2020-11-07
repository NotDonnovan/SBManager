from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('settings/clients', views.ClientSettings.as_view(), name='client_settings'),
    path('settings/add_client', views.new_client, name='new_client'),
    path('settings/clients/edit/<int:pk>', views.EditClient.as_view(), name='edit_client'),
    path('settings/add_device', views.new_device, name='new_device'),
    path('settings/categories', views.category_settings, name='categories'),
    path('settings/devices', views.DeviceSettings.as_view(), name='devices'),

]