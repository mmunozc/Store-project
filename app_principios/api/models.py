from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):

    COMPRADOR = 'comprador'
    VENDEDOR = 'vendedor'
    OPCIONES_TIPO = (
        (COMPRADOR, 'Comprador'),
        (VENDEDOR, 'Vendedor'),
    )

    telefono = models.IntegerField(default=0)
    direccion = models.CharField(max_length=30)
    establecimiento = models.CharField(max_length=30, default="n/a")
    tipo = models.CharField(
        max_length=10, choices=OPCIONES_TIPO, default=COMPRADOR)


class Producto(models.Model):

    nombre = models.CharField(max_length=30)
    precio = models.IntegerField()
    marca = models.CharField(max_length=15)
    disponibilidad = models.IntegerField(default=0)
    vendedor = models.ForeignKey(
        Usuario, related_name="productos", on_delete=models.CASCADE, null=True, blank=True)


class Orden(models.Model):

    comprador = models.ForeignKey(
        Usuario, related_name="orden_vend", on_delete=models.SET_NULL, blank=True, null=True)
    costo = models.IntegerField()
    cantidad = models.IntegerField(default=0)
    producto = models.ForeignKey(
        Producto, related_name="orden_prod", on_delete=models.SET_NULL, blank=True, null=True)
    completado = models.BooleanField(default=False)
