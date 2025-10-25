import uuid
from flask import Flask, jsonify, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from database import db
import os
from utils import validators
from datetime import datetime, timedelta
import hashlib
import filetype
from flask_cors import cross_origin

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET'])
def index():
    avisos = db.get_avisos(5)
    exito = request.args.get('exito')
    return render_template('index.html', avisos=avisos, exito=exito)

@app.route('/agregar-aviso', methods=['GET', 'POST'])
def agregar_aviso():
    if request.method == 'POST':
        region = request.form.get('region')
        comuna = request.form.get('comuna')
        sector = request.form.get('sector')
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        celular = request.form.get('celular')
        tipo = request.form.get('tipo')
        cantidad = request.form.get('cantidad')
        edad = request.form.get('edad')
        unidad = request.form.get('unidad')
        fecha_entrega_form = request.form.get('fecha-entrega')
        descripcion = request.form.get('descripcion')
        fotos = request.files.getlist('fotos')

        errores = validators.validate_aviso(region, comuna, sector, nombre, email, celular, tipo, cantidad, edad, unidad, fecha_entrega_form, descripcion)

        if not db.region_existe(region):
            errores.append("La región seleccionada no existe.")
        if not db.comuna_existe(comuna):
            errores.append("La comuna seleccionada no existe.")
        
        medios = ["whatsapp", "instagram", "telegram", "x", "tiktok", "otro"]
        contactos = []
        for medio in medios:
            if request.form.get(medio):
                identificador = request.form.get(f"{medio}-id")
                errores_contacto = validators.validate_contacto(medio, identificador)
                if errores_contacto:
                    errores.extend(errores_contacto)
                contactos.append((medio, identificador))
            
        for foto in fotos:
            if not validators.validate_foto(foto):
                errores.append("Foto inválida.")
        
        if errores:
            return render_template('agregar-aviso.html', errores=errores, form=request.form)
        else:
            unidad_medida = 'm' if unidad == 'meses' else 'a'
            fecha_entrega = datetime.strptime(fecha_entrega_form, '%Y-%m-%dT%H:%M')
            comuna_id= db.get_comuna_id(comuna)
            aviso_id = db.create_aviso(comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion)

            for medio, identificador in contactos:
                db.create_contacto(medio, identificador, aviso_id)
            
            for foto in fotos:
                _filename = hashlib.sha256(secure_filename(foto.filename).encode("utf-8")).hexdigest()
                _extension = filetype.guess(foto).extension
                img_filename = f"{_filename}_{str(uuid.uuid4())}.{_extension}"
                ruta = os.path.join('uploads', img_filename).replace('\\', '/')
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
                db.create_foto(ruta, img_filename, aviso_id)
            return redirect(url_for('index', exito="Aviso creado exitosamente."))
        
    return render_template('agregar-aviso.html')

@app.route('/ver-listado', methods=['GET'])
def ver_listado():
    pagina = request.args.get('pagina', 1, type=int)
    num = 5
    avisos, total = db.get_avisos_pagina(pagina, num)
    return render_template('ver-listado.html', avisos=avisos, total=total, pagina=pagina, num=num)

@app.route('/informacion-adopcion/<int:aviso_id>', methods=['GET'])
def informacion_adopcion(aviso_id):
    aviso, region, comuna, contactos, fotos = db.get_aviso_por_id(aviso_id)
    return render_template('informacion-adopcion.html', aviso=aviso, region=region, comuna=comuna, contactos=contactos, fotos=fotos)

@app.route('/ver-comentarios/<int:aviso_id>', methods=['GET'])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def ver_comentarios(aviso_id):
    comentarios = db.get_comentarios_por_aviso(aviso_id)
    data = []
    for comentario in comentarios:
        data.append({
            "nombre": comentario.nombre,
            "texto": comentario.texto,
            "fecha": comentario.fecha.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(data)
    
@app.route('/agregar-comentario', methods=['POST'])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def agregar_comentario():
    data = request.get_json()
    nombre = data.get('nombre', '').strip()
    texto = data.get('texto', '').strip()
    aviso_id = data.get('aviso_id')
    errores = validators.validate_comentario(nombre, texto)
    if errores:
        return jsonify({"success": False, "errores": errores}), 400
    
    db.create_comentario(nombre, texto, aviso_id)
    return jsonify({"success": True})

@app.route('/estadisticas', methods=['GET'])
def estadisticas():
    return render_template('estadisticas.html')

@app.route('/estadisticas/grafico_lineas', methods=['GET'])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def estadisticas_grafico_lineas():
    datos = db.get_avisos_por_dia()
    data = [{
        "date": r[0].strftime('%Y-%m-%d'),
        "count": r[1]
    } for r in datos]
    return jsonify(data)

@app.route('/estadisticas/grafico_torta', methods=['GET'])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def estadisticas_grafico_torta():
    datos = db.get_avisos_por_tipo()
    data = [{
        "type": r[0],
        "count": r[1]
    } for r in datos]
    return jsonify(data)

@app.route('/estadisticas/grafico_barras', methods=['GET'])
@cross_origin(origin="127.0.0.1", supports_credentials=True)
def estadisticas_grafico_barras():
    datos = db.get_adopciones_por_tipo_mes()
    tipos = {}
    meses_set = set()
    for r in datos:
        mes = r.mes
        tipo = r.tipo
        cantidad = r.cantidad
        meses_set.add(mes)
        tipos.setdefault(tipo, {})[mes] = cantidad
    
    meses = sorted(list(meses_set))

    series = []
    for tipo, cantidades in tipos.items():
        data = [cantidades.get(mes, 0) for mes in meses]
        series.append({
            "name": tipo,
            "data": data
        })
    return jsonify({"meses": meses,"series": series})
   