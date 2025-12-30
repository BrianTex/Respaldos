from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import Server
from django.contrib import messages


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
        Server.objects.create(
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