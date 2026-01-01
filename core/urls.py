from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('servers/', views.server_list, name='server_list'),
    path('servers/add/', views.add_server, name='add_server'),
    path('servers/<int:pk>/edit/', views.edit_server, name='edit_server'), 
    path('servers/<int:pk>/delete/', views.delete_server, name='delete_server'), 
    path('api/reportar/<int:server_id>',views.reportar,name='reportar'),
    path('api/listaReportes',views.listar_reportes,name='listaReportes'),
    path('servers/reportes',views.desplegar_async),
]
