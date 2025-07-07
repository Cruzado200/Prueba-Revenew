from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_and_optimize, name='optimizador_process'),
]