# Autor: Thomas Osorio

from django.urls import path
from .views import HomeView, EventoDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('evento/<int:pk>/', EventoDetailView.as_view(), name='detalle_evento'),
]
