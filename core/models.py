from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Server(models.Model):
    dominio_o_ip = models.CharField(max_length=255, unique=True, verbose_name="Dominio o IP")
    usuario_servidor = models.CharField(max_length=100, verbose_name="Usuario del Servidor")
    contrasena_bot = models.CharField(max_length=255, verbose_name="Contraseña del Bot")
 
    def __str__(self):
        return self.dominio_o_ip

    class Meta:
        verbose_name = "Servidor"
        verbose_name_plural = "Servidores"