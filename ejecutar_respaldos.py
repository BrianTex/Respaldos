import os
import django
import paramiko

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Respaldos.settings')
django.setup()

from core.models import ConfiguracionRespaldo

def realizar_respaldo():
    configuraciones = ConfiguracionRespaldo.objects.all()
    
    if not configuraciones:
        print("No hay configuraciones de respaldo pendientes.")
        return

    for conf in configuraciones:
        print(f"--- Iniciando respaldo: {conf} ---")
        try:
            # Configurar cliente SSH
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Conexión al servidor de ORIGEN
            # Asumimos que el modelo Server tiene ip, usuario y password
            ssh.connect(
                conf.servidor_origen.ip, 
                username=conf.servidor_origen.usuario, 
                password=conf.servidor_origen.password
            )
            
            # Comando para comprimir y enviar (ejemplo usando scp o rsync)
            # Aquí la lógica dependerá de cómo quieras mover los archivos
            comando = f"tar -czf - {conf.directorio_origen} | sshpass -p '{conf.servidor_destino.password}' ssh {conf.servidor_destino.usuario}@{conf.servidor_destino.ip} 'cat > {conf.directorio_destino}/respaldo_{conf.id}.tar.gz'"
            
            stdin, stdout, stderr = ssh.exec_command(comando)
            
            print(f"Respaldo completado para ID {conf.id}")
            ssh.close()
            
        except Exception as e:
            print(f"Error en respaldo {conf.id}: {e}")

if __name__ == "__main__":
    realizar_respaldo()
