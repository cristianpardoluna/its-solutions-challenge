from django.db import models
from backend import generate_token

class Person(models.Model):
    name = models.CharField(
        max_length=300,
        verbose_name="Nombre"
    )
    email = models.EmailField(
        verbose_name="Correo"
    )

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    owner = models.ForeignKey(
        to=Person,
        on_delete=models.CASCADE,
        verbose_name="Persona"
    )
    plate = models.CharField(
        max_length=6,
        verbose_name="Placa de patente"
    )
    brand = models.CharField(
        max_length=300,
        verbose_name="Marca"
    )
    color = models.CharField(
        max_length=300,
        verbose_name="Color"
    )

    def __str__(self):
        return self.plate

class Officer(models.Model):
    name = models.CharField(
        max_length=300,
        verbose_name="Nombre"
    )
    token = models.CharField(
        max_length=30,
        default=generate_token,
        verbose_name="Token"
    )

    def __str__(self):
        return self.name

class Infraction(models.Model):
    vehicle = models.ForeignKey(
        to=Vehicle,
        on_delete=models.DO_NOTHING,
        verbose_name="Vehículo"
    )
    comments = models.CharField(
        max_length=3000,
        verbose_name="Comentarios"
    )
    officer = models.ForeignKey(
        to=Officer,
        on_delete=models.CASCADE,
        verbose_name="Oficial"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Hora creación"
        )

    def __str__(self):
        return f"Infracción {self.vehicle.plate}"