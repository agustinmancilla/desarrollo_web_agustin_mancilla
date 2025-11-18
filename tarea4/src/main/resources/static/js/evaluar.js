function abrirModalEvaluacion(avisoId) {
    document.getElementById('avisoId').value = avisoId;
    document.getElementById('modalEvaluacion').style.display = 'flex';
}


function cerrarModal() {
    document.getElementById('modalEvaluacion').style.display = 'none';
}


function enviarEvaluacion() {
    const avisoId = document.getElementById('avisoId').value;
    const nota = parseInt(document.getElementById('nota').value);
    
    if (!nota || nota < 1 || nota > 7) {
        alert('Seleccionar una nota');
        return;
    }
    
    const formData = new FormData();
    formData.append('avisoId', avisoId);
    formData.append('nota', nota);
    
    fetch('/evaluar', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            cerrarModal();
            window.location.reload();
        } else {
            alert('Error al guardar la evaluación');
        }
    })
    .catch(error => {
        alert('Error al enviar la evaluación');
    });
}