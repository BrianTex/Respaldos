#!/bin/bash

id_origen="{{server_src.id}}"
origen="{{src_dir}}"
usuario_destino="{{dst_user}}"
ip_destino="{{server_dst.dominio_o_ip}}"
ruta_destino="{{dst_dir}}"
passwd_reporte="{{server_src.contrasena_bot}}"
url_reporte="http://{{ip_central}}:8000/api/reportar/${id_origen}/"

fecha_archivo="$(date +'%Y-%m-%d_%H-%M-%S')"
fecha_django="$(date +'%Y-%m-%d %H:%M:%S')"
archivo="respaldo_${fecha_archivo}.tar.gz"
ruta_temporal="/tmp/${archivo}"

tar -czf "$ruta_temporal" -C "$(dirname "$origen")" "$(basename "$origen")"

if [ $? -eq 0 ]; then
  SALIDA=$(rsync -av "$ruta_temporal" "${usuario_destino}@${ip_destino}:${ruta_destino}/" 2>&1)
  
  if [ $? -eq 0 ]; then
    estado="Respaldo exitoso"
  else
    estado="Error en rsync: $SALIDA"
  fi
  
  rm "$ruta_temporal"
else
  estado="Error al comprimir con tar"
fi

curl -X POST "$url_reporte" \
     -H "Autorizacion: $passwd_reporte" \
     -d "estado=${estado}" \
     -d "archivo=${archivo}" \
     -d "fecha=${fecha_django}"