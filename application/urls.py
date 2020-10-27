from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('settings/clients', views.client_settings, name='client_settings'),
    path('settings/add_client', views.new_client, name='new_client'),
]