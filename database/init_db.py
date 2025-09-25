from .conexion import Base, engine
from Entidades import init_entidades 


Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas en la base de datos")
