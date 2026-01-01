$(document).ready(function() {
    
    function cargarReportes() {
        $.get("/api/listaReportes", function(datos, status) {
            if (status === 'success') {
                let html = "";
                
                for (let i = 0; i < datos.length; i++) {
                    let claseFila = (datos[i].estado.toLowerCase() === 'éxito' || datos[i].estado.toLowerCase() === 'exito') 
                                    ? 'table-primary' 
                                    : 'table-danger';

                    html += `<tr class="${claseFila}">
                                <td>${datos[i].idServer}</td>
                                <td>${datos[i].archivo}</td>
                                <td>${datos[i].fecha}</td>
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