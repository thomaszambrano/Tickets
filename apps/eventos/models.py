# Autor: Thomas Osorio

from django.db import models
from django.db.models import F

class CategoriaEvento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Lugar(models.Model):
    nombre = models.CharField(max_length=150)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    latitud = models.FloatField(default=0.0)
    longitud = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.nombre} - {self.ciudad}"


class Evento(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    fecha = models.DateField()
    hora = models.TimeField()
    # Defaults para que Django pueda crear migraciones aunque la tabla exista con datos.
    # Luego se reemplazan con datos reales mediante seed (SQL).
    capacidad = models.PositiveIntegerField(default=0)
    organizador = models.CharField(max_length=150, default='')
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    categoria = models.ForeignKey(CategoriaEvento, on_delete=models.CASCADE, related_name='eventos')
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE, related_name='eventos')

    def __str__(self):
        return self.nombre


class TipoTicket(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name='tipos_ticket')
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre} — {self.evento.nombre}"



    def descontar_disponibilidad(self,cantidad):
        "descontamos de manera segura en la base de datos evitando race conditions"
        self.cantidad_disponibles = F('cantidad_disponible') -cantidad
        self.save(update_fields=['cantidad_disponible'])
        self.refresh_from_db() #Refrescamos el objeto con el valor real de la BD



    def restaurar_disponibilidad(self, cantidad):
        "retornamos disponibilidad de forma segura"
        self.cantidad_disponible = F('cantidad_disponible') + cantidad
        self.save(update_fields=['cantidad_disponible'])
        self.refresh_from_db()
         #Refrescamos el objeto con el valor real de la BD         
         