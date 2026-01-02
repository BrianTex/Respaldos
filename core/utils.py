from .models import Server
from django.template import Template,Context
from django.template.loader import render_to_string

def generar_script_personalizado(servidor, configuracion):
    contexto = {
        'servidor': servidor,
        'configuracion': configuracion,
        'ip_central': '192.168.1.10' 
    }
    script_final = render_to_string('scripts/respaldo_template.sh', contexto)
    
    return script_final

def automatizarServidor(Server,Configuracion):
    script=generar_script_personalizado(Server,Configuracion)
    