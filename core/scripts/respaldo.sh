#!/bin/bash

id_origen="{{server_src.id}}"
origen="{{src_dir}}"
usuario_destino="{{dst_user}}"
ip_destino="{{server_dst.dominio_o_ip}}"
ruta_destino="{{dst_dir}}"
passwd_reporte="{{server_src.contrasena_bot}}"
url_reporte="http://{{web_server_ip}}:8000/api/reportar/${id_origen}/"

fecha="$(date +%F)"
archivo="respaldo_${fecha}.tar.gz"

SALIDA=$(rsync -avz "$origen" "${usuario_destino}@${ip_destino}:${ruta_destino}/${archivo}" 2>&1)

if [ $? -eq 0 ]; then
  estado="El respaldo se realizó éxitosamente"
else
  estado="$SALIDA"
fi

curl -X POST "$url_reporte" -H "Authorization: $passwd_reporte" -d "estado=${estado}&archivo=${archivo}&fecha=${fecha}"