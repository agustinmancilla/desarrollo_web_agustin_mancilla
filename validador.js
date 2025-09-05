let fecha = new Date();
fecha.setHours(fecha.getHours()+3);
let year = fecha.getFullYear();
let month = String(fecha.getMonth() + 1).padStart(2, '0'); 
let day = String(fecha.getDate()).padStart(2, '0');
let hours = String(fecha.getHours()).padStart(2, '0');
let minutes = String(fecha.getMinutes()).padStart(2, '0');
let fechahoraform = `${year}-${month}-${day}T${hours}:${minutes}`;
document.getElementById("fecha-entrega").value = fechahoraform;

const validateName = (name) => {
    if(!name) return false;
    let lengthValid = name.trim().length <=200 && name.trim().length > 3;

    return lengthValid
};

const validateEmail = (email) => {
    if(!email) return false
    let lengthValid = email.length <=100;
    
    let re=/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    let formatValid = re.test(email);
    return lengthValid && formatValid;
};

const validateTel = (phone) => {
    let lengthValid = phone.length >=8 && phone.length <=15;

    let re = /^\+\d{3}\.\d{5,12}$/;
    let formatValid = re.test(phone);
    
    return lengthValid && formatValid;
}; 
const validateSector = (sector) => {
    if (sector){
        let lengthValid = sector.length <= 100;
        return lengthValid;
    }
    
    return true;
};

const validateSelect = (select) => {
    if(!select) return false;
    return true;
};

const validateQuantity = (quantity) => {
    if(!quantity) return false;
    let lengthValid = quantity >= 1;
    return lengthValid;
};

const validateDueDate = (date) =>{
    if(!date) return false;
    let re =/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/;
    let formatValid = re.test(date);
    let dateValid = date >= fechahoraform;
    return formatValid && dateValid;
};

const validatePetType = () => {
    let selected = document.querySelector('input[name="tipo"]:checked');
    if(!selected) return false;
    return true;
};

const validateUnitType = () => {
    let selected = document.querySelector('input[name="unidad"]:checked');
    if(!selected) return false;
    return true;
};

const validatePhotos = () => {
    let fotosInput = document.getElementById("fotos");
    return fotosInput && fotosInput.files && fotosInput.files.length > 0;
};

const validateForm = () => {
    let avisoForm = document.forms["avisoForm"];
    let nombre = avisoForm["nombre"].value;
    let email = avisoForm["email"].value;
    let celular = avisoForm["celular"].value;
    let fechaentrega = avisoForm["fecha-entrega"].value;
    let sector = avisoForm["sector"].value;
    let region = avisoForm["region"].value;
    let comuna = avisoForm["comuna"].value;
    let cantidad = avisoForm["cantidad"].value;
    let edad = avisoForm["edad"].value;


    let invalidInputs = [];
    let isValid = true;
    const setInvalidInput = (inputName) => {
      invalidInputs.push(inputName);
      isValid &&= false;
    };

    if(!validateName(nombre)){
        setInvalidInput("Nombre");
    }
    if(!validateEmail(email)){
        setInvalidInput("Email");
    }
    if(!validateTel(celular)){
        setInvalidInput("Teléfono");
    }
    if(!validateSector(sector)){
        setInvalidInput("Sector");
    }
    if(!validateSelect(region)){
        setInvalidInput("Región");
    }
    if(!validateSelect(comuna)){
        setInvalidInput("Comuna");
    }
    if(!validateQuantity(cantidad)){
        setInvalidInput("Cantidad");
    }
    if(!validateQuantity(edad)){
        setInvalidInput("Edad");
    }   
    if(!validateDueDate(fechaentrega)){
        setInvalidInput("Fecha de entrega");
    }   
    if(!validatePetType()){
        setInvalidInput("Tipo de mascota");
    }   
    if(!validateUnitType()){
        setInvalidInput("Unidad de edad");
    }
    if(!validatePhotos()){
        setInvalidInput("Fotos");
    }   
    let validationBox = document.getElementById("val-box");
    let validationMessageElem = document.getElementById("val-msg");
    let validationListElem = document.getElementById("val-list");
    let formContainer = document.querySelector(".main-container");

    if(!isValid){
        validationListElem.textContent = "";
        for (input of invalidInputs) {
            let listElement = document.createElement("li");
            listElement.innerText = input;
            validationListElem.append(listElement);
        }
        validationMessageElem.innerText = "Campos son inválidos:";
        validationBox.style.backgroundColor = "#ffdddd";
        validationBox.style.borderLeftColor = "#f44336";
        validationBox.hidden = false;
    }
    else{
        avisoForm.style.display = "none";
        validationMessageElem.innerText = "¿Está seguro que desea agregar este aviso de adopción?";
        validationListElem.textContent = "";
        validationBox.style.backgroundColor = "#ddffdd";
        validationBox.style.borderLeftColor = "#4CAF50";
        
        let submitButton = document.createElement("button");
        submitButton.innerText = "Sí, estoy seguro";
        submitButton.className = "boton-agregar"; 
        submitButton.style.marginRight = "10px";
        submitButton.addEventListener("click", () => {
            validationMessageElem.innerText = "Hemos recibido la información de adopción, muchas gracias y suerte";
            validationListElem.textContent = "";
            validationBox.style.backgroundColor = "#ddffdd";
            validationBox.style.borderLeftColor = "#4CAF50";
            let inicioButton = document.createElement("button");
            inicioButton.innerText = "volver al inicio";
            inicioButton.className = "boton-nav";
            inicioButton.addEventListener("click", () => {
                window.location.href="index.html"
            });
            validationListElem.appendChild(inicioButton); 
        });
        
        let backButton = document.createElement("button");
        backButton.innerText = "No, no estoy seguro, quiero volver al formulario";
        backButton.className = "boton-rechazar";
        backButton.addEventListener("click", () => {
            avisoForm.style.display = "block";
            validationBox.hidden = true;
        });
        validationListElem.appendChild(submitButton);
        validationListElem.appendChild(backButton);
        validationBox.hidden = false;
    }
};

let agregarBtn = document.getElementById("agregar-btn");
agregarBtn.addEventListener("click", validateForm);
