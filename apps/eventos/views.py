# Autor: Thomas Osorio

from django.views.generic import ListView, DetailView
from .models import Evento


class HomeView(ListView):
    model = Evento
    template_name = 'eventos/home.html'
    context_object_name = 'eventos'
    ordering = ['fecha']


class EventoDetailView(DetailView):
    model = Evento
    template_name = 'eventos/detalle_evento.html'
    context_object_name = 'evento'
