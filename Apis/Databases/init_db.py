from .conexion import Base, engine
from . import modelos

Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas en la base de datos")
