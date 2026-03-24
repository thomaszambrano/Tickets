# Autor: Thomas Osorio

from django.urls import path
from . import views

urlpatterns = [
    path('mis-reservas/', views.mis_reservas, name='mis_reservas'),
    path('crear/<int:evento_id>/', views.crear_reserva, name='crear_reserva'),
    path('cancelar/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
]
