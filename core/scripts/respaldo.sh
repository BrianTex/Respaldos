#!/bin/bash

id_origen="{{server.id}}"
origen="{{conf.origen}}"
usuario_destino="{{conf.usuario_destino}}"
ip_destino="{{conf.ip_destino}}"
ruta_destino="{{conf.ruta_destino}}"
passwd_reporte="{{server.contrasena_bot}}"
url_reporte="http://{{web_server_ip}}:8000/api/reportar/${id_origen}/"

fecha="$(date +%F)"
archivo="respaldo_${fecha}.tar.gz"

SALIDA=$(rsync -avz "$origen" "${usuario_destino}@${ip_destino}:${ruta_destino}/${archivo}" 2>&1)

if [ $? -eq 0 ]; then
  estado="éxito"
else
  estado="$SALIDA"
fi

curl -X POST "$url_reporte" -H "Authorization: $passwd_reporte" -d "estado=${estado}&archivo=${archivo}&fecha=${fecha}"