function revisaCheck(element){
                const checkboxes = document.querySelectorAll('input[type="checkbox"]');
                let selected = 0;
                for (let i = 0; i< checkboxes.length; i++){
                    if (checkboxes[i].checked){
                        selected++;
                    }
                }
                if(element.checked && selected > 5){
                    element.checked = false;
                }
                if (element.checked) {
                document.getElementById(element.name).style.display = "block";
                } else {
                document.getElementById(element.name).style.display = "none";
                }
}    
function agregarFoto(){
                const contenedor = document.getElementById("foto-container");
                const inputs= contenedor.querySelectorAll('input[type="file"]');
                if(inputs.length >= 5){
                    return;
                }
               
                const nuevoInput = document.createElement("input");
                nuevoInput.type= "file";
                nuevoInput.name= "fotos";
                nuevoInput.id="fotos";
                nuevoInput.accept="image/*";
                contenedor.appendChild(nuevoInput);
                contenedor.appendChild(document.createElement("br"));
}


document.getElementById("agregar-foto").addEventListener("click", agregarFoto);



