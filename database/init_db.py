from database.db import engine, Base
from database.models import Region, Comuna, Miembro, Actividad, Foto

def create_tables():
    print("Conectando con MySQL y analizando modelos...")
    # make sure to import all models here so that they are registered with SQLAlchemy
    Base.metadata.create_all(bind=engine)
    print("¡Arquitectura de tablas generada exitosamente en tarea2_appweb!")

if __name__ == "__main__":
    create_tables()