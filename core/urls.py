from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('servers/', views.server_list, name='server_list'),
    path('servers/add/', views.add_server, name='add_server'),
    path('servers/<int:pk>/edit/', views.edit_server, name='edit_server'), # Placeholder
    path('servers/<int:pk>/delete/', views.delete_server, name='delete_server'), # Placeholder
]
