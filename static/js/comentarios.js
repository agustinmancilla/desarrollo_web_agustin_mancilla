document.addEventListener('DOMContentLoaded', function() {

    const avisoId = parseInt(window.location.pathname.split('/').pop());
    const form = document.getElementById('comentario-form');
    const comentariosList = document.getElementById('comentarios-list');

    cargarComentarios();

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        agregarComentario();
    });

    async function cargarComentarios() {
        const response = await fetch(`${window.location.origin}/ver-comentarios/${avisoId}`);
        const comentarios = await response.json();

        if (comentarios.length === 0) {
            comentariosList.innerHTML = '<p>No hay comentarios.</p>';
            return;
        }

        let html = `<h4>Comentarios</h4>`;
        for (let comentario of comentarios) {
            html += `
                <div class="comentario-item">
                    <strong>${comentario.nombre}</strong> <em>(${new Date(comentario.fecha).toLocaleString()})</em>
                    <p>${comentario.texto}</p>
                </div>
            `;
        }
        comentariosList.innerHTML = html;
    }

    async function agregarComentario() {
        const nombre = document.getElementById('nombre').value.trim();
        const texto = document.getElementById('texto').value.trim();

        const response = await fetch(`${window.location.origin}/agregar-comentario`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nombre: nombre, texto: texto, aviso_id: avisoId })
        });

        const data = await response.json();

        if (data.success) {
            form.reset();
            cargarComentarios();
        } else {
            alert('Error: ' + data.errores.join('\n'));
        }
    }
});
