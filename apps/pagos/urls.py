# Author: Juan José Baron Osorio
from django.urls import path
from . import views

urlpatterns = [
    path('crear/<int:reserva_id>/', views.crear_pago, name='crear_pago'),
    path('ticket/<int:ticket_id>/pdf/', views.descargar_ticket, name='descargar_ticket'),
]
