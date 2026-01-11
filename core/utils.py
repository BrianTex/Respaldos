from .models import Server
from django.template import Template, Context
from django.template.loader import render_to_string
import paramiko

def generar_script_personalizado(conf):
    contexto = {
        'server_src': conf.servidor_origen,
        'server_dst': conf.servidor_destino,
        'src_dir': conf.directorio_origen,
        'dst_dir': conf.directorio_destino,
        'dst_user': conf.dst_user,
        'ip_central': '127.0.0.1' 
    }
    script_final = render_to_string('scripts/respaldo.sh', contexto)    
    return script_final

def automatizar_con_llave(conf, script):
    origen = conf.servidor_origen 
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    ssh.connect(
        origen.dominio_o_ip, 
        username=origen.usuario_servidor, 
        look_for_keys=True
    )
    sftp = ssh.open_sftp()
    ruta_script = f"/home/{origen.usuario_servidor}/respaldo_bot.sh"
    
    with sftp.file(ruta_script, 'w') as f:
        f.write(script)
    sftp.close()
    ssh.exec_command(f"chmod +x {ruta_script}")

    linea_cron = f"{conf.frecuencia_cron} {ruta_script}"
    comando_cron = f'{{ crontab -l 2>/dev/null; echo "{linea_cron}"; }} | sort -u | crontab -'

    stdin, stdout, stderr = ssh.exec_command(comando_cron)
    error_cron = stderr.read().decode()

    if error_cron:
        print(f"Error: {error_cron}")
    ssh.close()

def automatizarServidor(conf):
    script = generar_script_personalizado(conf)
    automatizar_con_llave(conf, script)

def deleteConf(conf):
    origen = conf.servidor_origen 
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    ssh.connect(
        origen.dominio_o_ip, 
        username=origen.usuario_servidor, 
        look_for_keys=True
    )
    ruta_script = f"/home/{origen.usuario_servidor}/respaldo_bot.sh"
    ssh.exec_command(f"rm {ruta_script}")
    comando_limpiar = f'{{ crontab -l 2>/dev/null; }} | grep -v "{ruta_script}" | crontab -'
    ssh.exec_command(comando_limpiar)
    ssh.close()