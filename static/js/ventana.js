function abrir(src){
    const modal = document.getElementById("ventana-foto");
    const img = document.getElementById("imagen-ampliada");
    img.src = src;
    modal.style.display = "flex";
    const info = document.getElementById("info");
    info.style.display = "none";
}

function cerrar(){
    const modal = document.getElementById("ventana-foto");
    modal.style.display = "none";
    const info = document.getElementById("info");
    info.style.display = "block";
}


document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".img-detalle").forEach(img => {
        img.addEventListener("click", () => abrir(img.src));
    });
    const btn = document.getElementById("cerrar-vent-btn");
    if (btn) btn.addEventListener("click", cerrar);
});