$(document).ready(function() {
    
    function cargarReportes() {
        $.get("/api/listaReportes/", function(datos, status) {
            if (status === 'success') {
                console.log(datos);
                
                let html = "";
                
                for (let i = 0; i < datos.length; i++) {
                    let claseFila = (datos[i].estado) === 'Respaldo exitoso'
                                    ? 'table-primary' 
                                    : 'table-danger';
                    let fechaObjeto = new Date(datos[i].fecha.replace('Z', ''));         
                    let fechaFormateada = fechaObjeto.toLocaleString('es-ES', {
                        day: '2-digit',
                        month: '2-digit',
                        year: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit',
                        second: '2-digit'
                    });  
                    html += `<tr class="${claseFila}">
                                <td>${datos[i].idServer}</td>
                                <td>${datos[i].archivo}</td>
                                <td>${fechaFormateada}</td>
                                <td><strong>${datos[i].estado}</strong></td>
                             </tr>`;
                }
                
                if (datos.length === 0) {
                    html = "<tr><td colspan='4' class='text-center'>No hay reportes registrados</td></tr>";
                }

                $("#tabla-reportes").html(html);
            }
        });
    }

    cargarReportes();
    setInterval(cargarReportes, 10000);
});