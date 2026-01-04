from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Server,Reporte
from django.contrib import messages
from django.http import JsonResponse
from .models import ConfiguracionRespaldo
from .utils import automatizarServidor

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def server_list(request):
    servers = Server.objects.all()
    return render(request, 'server_list.html', {'servers': servers})

@login_required
def add_server(request):
    if request.method == 'POST':
        # Extracción manual de los datos del formulario
        dominio = request.POST.get('dominio_o_ip')
        usuario = request.POST.get('usuario_servidor')
        contrasena = request.POST.get('contrasena_bot')

        # Validación simple
        if not dominio or not usuario or not contrasena:
            messages.error(request, 'Todos los campos son obligatorios.')
            # Devolvemos los datos ingresados para que el usuario no los pierda
            return render(request, 'add_server.html', {
                'dominio_o_ip': dominio,
                'usuario_servidor': usuario,
            })
        
        # Creación del objeto
        nuevoServer=Server.objects.create(
            dominio_o_ip=dominio,
            usuario_servidor=usuario,
            contrasena_bot=contrasena
        )
        messages.success(request, 'Servidor añadido exitosamente.')
        return redirect('server_list')

    return render(request, 'add_server.html')

@login_required
def edit_server(request, pk):
    server = get_object_or_404(Server, pk=pk)
    if request.method == 'POST':
        # Extracción manual de los datos
        dominio = request.POST.get('dominio_o_ip')
        usuario = request.POST.get('usuario_servidor')
        # La contraseña es opcional al editar; si está en blanco, no se cambia
        contrasena = request.POST.get('contrasena_bot')

        # Validación
        if not dominio or not usuario:
            messages.error(request, 'Los campos de dominio y usuario son obligatorios.')
            return render(request, 'edit_server.html', {'server': server})

        # Actualización del objeto
        server.dominio_o_ip = dominio
        server.usuario_servidor = usuario
        if contrasena: # Solo actualiza la contraseña si el usuario ingresó una nueva
            server.contrasena_bot = contrasena
        server.save()

        messages.success(request, 'Servidor actualizado exitosamente.')
        return redirect('server_list')
        
    return render(request, 'edit_server.html', {'server': server})

@login_required
def delete_server(request, pk):
    server = get_object_or_404(Server, pk=pk)
    if request.method == 'POST':
        server.delete()
        messages.success(request, 'Servidor eliminado exitosamente.')
        return redirect('server_list')
    return render(request, 'delete_server_confirm.html', {'server': server})

#View que recibe la informaciòn mandada por el script 
def reportar(request,server_id):
    if request.method=='POST':
        token=request.POST.get('Autorizacion')
        try:
            servidor=Server.objects.get(id=server_id)
            if servidor.password_bot!=token:
                return JsonResponse({'error': 'Token inválido'}, status=403)
            
            estado=request.POST.get('estado')
            archivo=request.POST.get('archivo')
            fecha=request.POST.get('fecha')

            Reporte.objects.create(
                estado=estado,
                archivo=archivo,
                fecha=fecha,
                idServidor=server_id
            )
            return JsonResponse({'status': 'recibido'})
        except Server.DoesNotExist:
            return JsonResponse({'error': 'Servidor no encontrado'}, status=404)


def serializar_a_json(querySet):
    datos = []
    for registro in querySet:
        d = {}
        d['estado'] = registro.estado
        d['archivo'] = registro.address
        d['fecha']  = registro.city
        d['idServer'] = registro.idServer
        datos.append(d)
    return datos

def listar_reportes(request):
    reportes = Reporte.objects.all()
    return JsonResponse(serializar_a_json(reportes), safe=False)

@login_required
def desplegar_async(request):
    t = 'reportes.html'
    return render(request, t)

@login_required
def add_configuracion(request):
    if request.method == 'POST':
        servidor_origen_id = request.POST.get('servidor_origen')
        servidor_destino_id = request.POST.get('servidor_destino')
        dir_origen = request.POST.get('directorio_origen')
        dir_destino = request.POST.get('directorio_destino')
        cron = request.POST.get('frecuencia_cron')
        dst_user=request.POST.get('dst_user')

        origen = Server.objects.get(id=servidor_origen_id)
        destino = Server.objects.get(id=servidor_destino_id)

        nueva_conf = ConfiguracionRespaldo(
            servidor_origen=origen,
            servidor_destino=destino,
            directorio_origen=dir_origen,
            directorio_destino=dir_destino,
            frecuencia_cron=cron,
            dst_user=dst_user
        )
        nueva_conf.save()
        automatizarServidor(nueva_conf)
        return redirect('servers_list') 

    servidores = Server.objects.all()
    return render(request, 'add_configuracion.html', {'servidores': servidores})

@login_required
def delete_configuracion(request, pk):
    # Buscamos la configuración o lanzamos un 404 si no existe
    config = get_object_or_404(ConfiguracionRespaldo, pk=pk)
    
    if request.method == 'POST':
        config.delete()
        messages.success(request, 'Configuración de respaldo eliminada correctamente.')
        return redirect('server_list') # O a la lista de configuraciones si ya la tienes
        
    return render(request, 'delete_config_confirm.html', {'config': config})

@login_required
def configuracion_list(request):
    configuraciones = ConfiguracionRespaldo.objects.all()
    return render(request, 'configuracion_list.html', {'configuraciones': configuraciones})