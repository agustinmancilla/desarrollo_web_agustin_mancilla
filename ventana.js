function abrir(){
    document.getElementById("ventana-foto").style.display= "block";
    document.getElementById("info").style.display="none";
}   
function cerrar(){
    document.getElementById("ventana-foto").style.display= "none";
    document.getElementById("info").style.display="block";
}
document.getElementById("imagen").addEventListener("click", abrir);
document.getElementById("cerrar-vent-btn").addEventListener("click", cerrar);