from sqlalchemy import Column, Integer, String, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from database.db import Base

# --- Table region y comuna ---
class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    
    comunas = relationship("Comuna", back_populates="region")

class Comuna(Base):
    __tablename__ = 'comuna'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    
    region = relationship("Region", back_populates="comunas")
    miembros = relationship("Miembro", back_populates="comuna")

# --- Table miembro ---
class Miembro(Base):
    __tablename__ = 'miembro'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    email = Column(String(80), nullable=False, unique=True)
    telefono = Column(String(15), nullable=False)
    categoria = Column(String(50), nullable=False) # estudiante, funcionario o academico
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    
    comuna = relationship("Comuna", back_populates="miembros")
    actividades = relationship("Actividad", back_populates="miembro", cascade="all, delete-orphan")

class Actividad(Base):
    __tablename__ = 'actividad'
    id = Column(Integer, primary_key=True, autoincrement=True)
    miembro_id = Column(Integer, ForeignKey('miembro.id'), nullable=False)

    tipo = Column(String(255), nullable=False) # Aquí guardaremos el JSON de los checkboxes
    descripcion = Column(Text, nullable=False)
    dias_semana = Column(Integer, nullable=False)
    horas_dia = Column(Float, nullable=False)
    enlace = Column(String(300), nullable=True) # Opcional
    año_ingreso = Column(Integer, nullable=True) 
    telegram = Column(String(100), nullable=True)
    cargo = Column(String(100), nullable=True)
    area = Column(String(100), nullable=True)
    ramos = Column(String(255), nullable=True)
    investigacion = Column(String(255), nullable=True)
    
    miembro = relationship("Miembro", back_populates="actividades")
    fotos = relationship("Foto", back_populates="actividad", cascade="all, delete-orphan")

class Foto(Base):
    __tablename__ = 'foto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)
    
    actividad = relationship("Actividad", back_populates="fotos")