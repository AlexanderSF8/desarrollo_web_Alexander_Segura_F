from database.db import engine, Base
from database.models import Miembro, Actividad, Foto

print("Iniciando el reinicio de la base de datos...")

#  ESTO BORRA TODAS LAS TABLAS Y SUS DATOS
Base.metadata.drop_all(bind=engine)
print("Tablas antiguas y datos de prueba eliminados.")

# ESTO CREA LAS TABLAS DE NUEVO CON LA REGLA CASCADE
Base.metadata.create_all(bind=engine)
print("Tablas nuevas creadas con éxito. ¡Base de datos limpia y lista!")