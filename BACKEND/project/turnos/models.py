from django.db import models
from django.conf import settings

class Turno(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADO', 'Confirmado'),
        ('CANCELADO', 'Cancelado'),
        ('COMPLETADO', 'Completado'),
    )
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='turnos',
        null=True, # In case some appointments are walked-in (though app logic says otherwise, safe default)
        blank=True
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    fecha = models.DateField()
    hora = models.TimeField()
    descripcion = models.TextField(blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.marca} {self.modelo} ({self.fecha} {self.hora})"
