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
    
class Reporte(models.Model):
    estado= models.CharField(max_length=100,verbose_name='Estado del servidor')
    archivo=models.CharField(max_length=50,verbose_name='Nombre del archivo o directorio')
    fecha=models.DateTimeField()
    idServer=models.ForeignKey(Server, on_delete=models.CASCADE)


class ConfiguracionRespaldo(models.Model):
    servidor_origen = models.ForeignKey(
        Server, 
        on_delete=models.CASCADE, 
        related_name='respaldos_origen',
        verbose_name="Servidor Origen"
    )

    servidor_destino = models.ForeignKey(
        Server, 
        on_delete=models.CASCADE, 
        related_name='respaldos_destino',
        verbose_name="Servidor Destino"
    )
    
    directorio_origen = models.CharField(
        max_length=255, 
        verbose_name="Directorio a respaldar (Origen)"
    )
    directorio_destino = models.CharField(
        max_length=255, 
        verbose_name="Directorio donde guardar (Destino)"
    )
    
    frecuencia_cron = models.CharField(
        max_length=100,
        verbose_name="Frecuencia (Cron)",
        help_text="Formato: min hora dia mes dia_semana (ej: 0 3 * * *)"
    )
    dst_user=models.CharField(
        max_length=50,
        verbose_name="Usuario destino",
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Respaldo de {self.servidor_origen} a {self.servidor_destino}"

    class Meta:
        verbose_name = "Configuración de Respaldo"
        verbose_name_plural = "Configuraciones de Respaldo"