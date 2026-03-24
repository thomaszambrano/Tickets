# Autor: Thomas Osorio

from django.urls import path
from .views import EventoDetailView, EventoListView, HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('eventos/', EventoListView.as_view(), name='catalogo_eventos'),
    path('evento/<int:pk>/', EventoDetailView.as_view(), name='detalle_evento'),
]
