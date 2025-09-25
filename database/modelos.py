from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .conexion import Base

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .conexion import Base

class Proveedor(Base):
    __tablename__ = "Proveedores"
    Nit = Column(Integer, primary_key=True, index=True)
    Nombre = Column(String(100), nullable=False)
    Direccion = Column(String(120), index=True)
    Telefono = Column(String(20))

    # Un proveedor tiene muchos libros
    libros = relationship("Libro", back_populates="proveedor")


class Libro(Base):
    __tablename__ = "libros"
    Codigo_Libro = Column(Integer, primary_key=True, index=True)
    Titulo = Column(String(200), nullable=False)
    Autor = Column(String(100))
    Año = Column(Integer)
    Precio = Column(Float)
    Nit_Proveedor = Column(Integer, ForeignKey("Proveedores.Nit"))

    # Cada libro pertenece a un proveedor
    proveedor = relationship("Proveedor", back_populates="libros")



