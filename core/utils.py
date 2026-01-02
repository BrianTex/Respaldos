from .models import Server
from django.template import Template,Context
from django.template.loader import render_to_string
import paramiko
def generar_script_personalizado(servidor, configuracion):
    contexto = {
        'servidor': servidor,
        'configuracion': configuracion,
        'ip_central': '192.168.1.10' 
    }
    script_final = render_to_string('scripts/respaldo_template.sh', contexto)
    
    return script_final

def automatizar_con_llave(Server, Configuracion, script):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    ssh.connect(
        Server.dominio_o_ip, 
        username=Server.usuario_servidor, 
        look_for_keys=True
    )
    sftp = ssh.open_sftp()
    ruta_script = f"/home/{Server.usuario_servidor}/respaldo_bot.sh"
    
    with sftp.file(ruta_script, 'w') as f:
        f.write(script)
    sftp.close()
    ssh.exec_command(f"chmod +x {ruta_script}")

    linea_cron = f"{Configuracion.cron} {ruta_script}"
    comando_cron = f'(crontab -l 2>/dev/null; echo "{linea_cron}") | crontab -'
    ssh.exec_command(comando_cron)
    ssh.close()

def automatizarServidor(Server,Configuracion):
    script=generar_script_personalizado(Server,Configuracion)
    automatizar_con_llave(Server,Configuracion,script)