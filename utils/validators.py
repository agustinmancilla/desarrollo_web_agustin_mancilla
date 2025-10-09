import re
from datetime import datetime, timedelta

import filetype

def validate_name(name):
    if not name:
        return False
    trimmed = name.strip()
    return 3 < len(trimmed) <= 200

def validate_email(email):
    if not email:
        return False
    length_valid = len(email) <= 100
    pattern = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    format_valid = re.match(pattern, email) is not None
    return length_valid and format_valid

def validate_tel(phone):
    length_valid = 8 <= len(phone) <= 15
    pattern = r'^\+\d{3}\.\d{5,12}$'
    format_valid = re.match(pattern, phone) is not None
    return length_valid and format_valid
    
def validate_sector(sector):
    if sector:
        return len(sector) <= 100
    return True

def validate_select(select):
    return bool(select)

def validate_quantity(quantity):
    if quantity is None:
        return False
    q = int(quantity)
    if q >= 1:
        return True
    return False

def validate_due_date(date):
    pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$'
    if not re.fullmatch(pattern, date):
        return False
    
    date_a = datetime.strptime(date, '%Y-%m-%dT%H:%M')
    date_plus_3 = datetime.now() + timedelta(hours=3)
    return date_a >= date_plus_3

def validate_pet_type(tipo):
    return tipo in {'perro', 'gato'}

def validate_unit_type(unidad):
    return unidad in {'meses', 'años'}

def validate_text(text):
    if re.search(r'<[^>]*>', text):
        return False
    return True

def validate_contact_method(method):
    return method in {'whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'}   


def validate_foto(foto):
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
    ALLOWED_MIMETYPES = {"image/jpeg", "image/png", "image/gif"}
    if foto is None:
        return False

    if foto.filename == "":
        return False
        
    ftype_guess = filetype.guess(foto)
    if ftype_guess.extension not in ALLOWED_EXTENSIONS:
        return False
    
    if ftype_guess.mime not in ALLOWED_MIMETYPES:
        return False
    return True

def validate_aviso(region, comuna, sector, nombre, email, celular, tipo, cantidad, edad, unidad, fecha_entrega, descripcion):
    errores = []
    if not validate_select(region):
        errores.append("Región inválida.")
    if not validate_select(comuna):
        errores.append("Comuna inválida.")
    if not validate_sector(sector):
        errores.append("Sector inválido.")
    if not validate_name(nombre):
        errores.append("Nombre inválido.")
    if not validate_email(email):
        errores.append("Email inválido.")
    if not validate_tel(celular):
        errores.append("Teléfono inválido.")
    if not validate_pet_type(tipo):
        errores.append("Tipo de mascota inválido.")
    if not validate_quantity(cantidad):
        errores.append("Cantidad inválida.")
    if not validate_quantity(edad):
        errores.append("Edad inválida.")
    if not validate_unit_type(unidad):
        errores.append("Unidad de edad inválida.")
    if not validate_due_date(fecha_entrega):
        errores.append("Fecha de entrega inválida.")
    if not validate_text(descripcion):
        errores.append("Descripción inválida.")

    return errores

def validate_contacto(metodo, identificador):
    errores = []
    if not validate_contact_method(metodo):
        errores.append("Método de contacto inválido.")
    if not validate_text(identificador):
        errores.append("Identificador inválido.")
    return errores