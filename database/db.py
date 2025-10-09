from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BigInteger, DATETIME, VARCHAR, Enum, Text
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = "3306"

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    
    comunas = relationship("Comuna", back_populates="region")

class Comuna(Base):
    __tablename__ = 'comuna'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    
    region = relationship("Region", back_populates="comunas")
    avisos = relationship("Aviso_adopcion", back_populates="comuna")
class Aviso_adopcion(Base):
    __tablename__ = 'aviso_adopcion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_ingreso = Column(DATETIME, nullable=False)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    sector = Column(VARCHAR(100), nullable=True)
    nombre = Column(VARCHAR(200), nullable=False)
    email = Column(VARCHAR(100), nullable=False)
    celular = Column(VARCHAR(15), nullable=True)
    tipo = Column(Enum('gato', 'perro'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    edad = Column(Integer, nullable=False)
    unidad_medida = Column(Enum('a', 'm'), nullable=False)
    fecha_entrega = Column(DATETIME, nullable=False)
    descripcion = Column(VARCHAR(500), nullable=True)

    comuna = relationship("Comuna", back_populates="avisos")
    fotos = relationship("Foto", back_populates="aviso")
    contactar_por = relationship("Contactar_Por", back_populates="aviso")

class Foto(Base):
    __tablename__ = 'foto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(VARCHAR(300), nullable=False)
    nombre_archivo = Column(VARCHAR(300), nullable=False)
    aviso_id = Column(Integer, ForeignKey('aviso_adopcion.id'), primary_key=True, nullable=False)

    aviso = relationship("Aviso_adopcion", back_populates="fotos")

class Contactar_Por(Base):
    __tablename__ = 'contactar_por'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable=False)
    identificador = Column(VARCHAR(150), nullable=False)
    aviso_id = Column(Integer, ForeignKey('aviso_adopcion.id'), primary_key=True, nullable=False)

    aviso = relationship("Aviso_adopcion", back_populates="contactar_por")


def get_avisos(num):
    session = SessionLocal()
    avisos = session.query(Aviso_adopcion).order_by(Aviso_adopcion.id.desc()).limit(num).all()
    resultado= []
    for aviso in avisos:
        comuna = session.query(Comuna).filter_by(id=aviso.comuna_id).first()
        fotos= session.query(Foto).filter_by(aviso_id=aviso.id).all()
        resultado.append((aviso, comuna.nombre, fotos))
    session.close()
    return resultado

def get_avisos_pagina(pagina, num):
    session = SessionLocal()
    offset = (pagina - 1) * num
    avisos = session.query(Aviso_adopcion).order_by(Aviso_adopcion.id.desc()).offset(offset).limit(num).all()
    total = session.query(Aviso_adopcion).count()
    resultado= []
    for aviso in avisos:
        comuna = session.query(Comuna).filter_by(id=aviso.comuna_id).first()
        fotos= session.query(Foto).filter_by(aviso_id=aviso.id).all()
        resultado.append((aviso, comuna.nombre, fotos))
    session.close()
    return resultado, total

def get_aviso_por_id(aviso_id):
    session = SessionLocal()
    aviso = session.query(Aviso_adopcion).filter_by(id=aviso_id).first()
    comuna = session.query(Comuna).filter_by(id=aviso.comuna_id).first()
    region = session.query(Region).filter_by(id=comuna.region_id).first()
    contactos = session.query(Contactar_Por).filter_by(aviso_id=aviso.id).all() 
    fotos = session.query(Foto).filter_by(aviso_id=aviso.id).all()
    session.close()
    return aviso, region, comuna, contactos, fotos

def get_comuna_id(nombre):
    session = SessionLocal()
    comuna = session.query(Comuna).filter_by(nombre=nombre).first()
    session.close()
    return comuna.id
def comuna_existe(nombre_comuna):
    session = SessionLocal()
    existe = session.query(Comuna).filter_by(nombre=nombre_comuna).first() is not None
    session.close()
    return existe

def region_existe(nombre_region):
    session = SessionLocal()
    existe = session.query(Region).filter_by(nombre=nombre_region).first() is not None
    session.close()
    return existe

def create_aviso(comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion):
    session = SessionLocal()
    nuevo_aviso = Aviso_adopcion(
        fecha_ingreso = datetime.now(),
        comuna_id = comuna_id,
        sector = sector,
        nombre = nombre,
        email = email,
        celular = celular,
        tipo = tipo,
        cantidad = cantidad,
        edad = edad,
        unidad_medida = unidad_medida,
        fecha_entrega = fecha_entrega,
        descripcion = descripcion
    )
    session.add(nuevo_aviso)
    session.commit()
    nuevo_aviso_id= nuevo_aviso.id
    session.close()
    return nuevo_aviso_id

def create_foto(ruta_archivo, nombre_archivo, aviso_id):
    session = SessionLocal()
    nueva_foto = Foto(
        aviso_id = aviso_id,
        ruta_archivo = ruta_archivo,
        nombre_archivo = nombre_archivo
    )
    session.add(nueva_foto)
    session.commit()
    session.close()

def create_contacto(nombre, identificador, aviso_id):
    session = SessionLocal()
    nuevo_contacto = Contactar_Por(
        aviso_id = aviso_id,
        nombre = nombre,
        identificador = identificador
    )
    session.add(nuevo_contacto)
    session.commit()
    session.close()