from sqlalchemy import Column, String, Integer, LargeBinary, TIMESTAMP, func, Boolean, Text, ARRAY
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Usuarios(Base):
    __tablename__ = "USUARIOS"
    usuario = Column(String, primary_key=True)
    clave = Column(LargeBinary, nullable=False)


class DatosSensibles(Base):
    __tablename__ = "DATOS_SENSIBLES"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key_name = Column(String, nullable=False)
    value = Column(LargeBinary, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)


class CondicionesManuales(Base):
    __tablename__ = 'CONDICIONES_MANUALES'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    seleccionado = Column(Boolean, nullable=False, default=False)


class Evento(Base):
    __tablename__ = 'EVENTOS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Text, nullable=False)
    descripcion = Column(Text, nullable=False)
    dispositivo_origen = Column(Text, nullable=False)
    tipo = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    titulo = Column(Text, nullable=False)
    canal_notificacion = Column(Text, nullable=True, default="CanalVigilancia")
    destinatarios = Column(ARRAY(Text), nullable=True)


class Escenarios(Base):
    __tablename__ = 'ESCENARIOS'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Columna id
    nombre = Column(String, nullable=False)  # Columna nombre
    descripcion = Column(String, nullable=False)


class Acciones(Base):
    __tablename__ = 'ACCIONES'
    escenario = Column(Integer, primary_key=True)
    id_dispositivo = Column(String, nullable=False)
    comando = Column(String, nullable=False)
    orden = Column(Integer, primary_key=True)


class EventoCondicionEscenario(Base):
    __tablename__ = 'EVENTO_CONDICION_ESCENARIO'
    evento = Column(Integer, primary_key=True)
    condicion = Column(Integer, primary_key=True)
    escenario = Column(Integer, primary_key=True)
