Titulo : Sistema de gestion Bibliotecaria

Descripcion general: El sistema cuenta con la capacidad de automatizar procesos bibliotecarios, como lo son: -Apartado de libro: Permite la interaccion con cada uno de los libros que se encuentran en el sistemas y desarrolla funciones que permiten una gestion optima de l biblioteca (Crea, Actualiza, Elimina y presenta los libros). -Apartado de usuarios: Permite la el conteo y gestion de los usuarios que interactuan con el sistema, presenta de una forma ordenada el historial/Registro de los que se encuentran en el sistema. -Apartado de Prestamo: Permite llevar un registro o un control de las transacciones realizadas por los usuarios sobre los libros de los que dispone la biblioteca.

¿Porque es util y a que problemas responde? Es un sistema muy optimo puesto que facilita el manejo y el flujo de la informacion dentro del establecimiento, presenta de manera clara los movimientos que ocurren en el mismo, ademas de que elimina la necesidad antigua de un historial manual, transformandolo y llevandolo a un sistema detallado, ordenado, de facil acceso y manejo. Centraliza la información de manera que elimina el error humano de llevar las cuentas en diferentes campos de registro y lo transfiere a una sola, generando mas precision y anticipando futuros problemas por la redundancia de la informacion en el flujo de la misma. Ademas, Agiliza procesos de búsqueda, registro, préstamo y devolución ya que elimina la necesidad humana de busqueda por estanterias, automatiza la disponibilidad del libro y lleva un conteo automatico de la cantidad de ejemplares que hay de un libro.

Estructura de carpetas

Apis/main.py: Archivo Central/Principal de la Api, posee el desarrollo logico de la biblioteca.
Datos/Libros: Script que simula la base de datos de los libros ue hay el sistema (De momento se encuentra fuera de uso).
requirements.txt: Se encuentra la lista de dependencias usadas en la creacion del programa.
README.md: Documentacion e informacion sobre el proyecto.
Requisitos de Instalación -Python: Version 3.10 o superiores (En este caso 3.10.11). -fastapi: Version 0.100.0 o superiores (En este caso 0.116.1). -uvicorn: Version 0.23.0 o superiores (En este caso 0.35.0). -pydantic: Version 1.10.0 o superiores (En este caso 2.11.7).

Instrucciones de Ejecución 1)Instalar las dependencias fastapi, uvicorn, pydantic. 1.1)Abrir la terminal en la carpeta donde está tu archivo main.py. 2) Ejecutar el servidor con: uvicorn main:app --reload o python -m uvicorn main:app 3) Si se ejecuta correctamente saldra: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit) 4) Damos CTRL+C en el http y nos llevara a un apartado en nuestro navegador 5) Editamos el enlace de manera: http://127.0.0.1:8000/docs ---> /docs 6) Una vez en el apartado, se prueban los endpoints seleccionando cada uno e inicializando con el "try it out" en cada endpoint

Descripción de Endpoints

Usuarios: Get/Usuarios: Lista todos los usuarios Get/Usuarios/{cedula}: Consulta un usuario por su cédula Post/Usuarios: Crea un nuevo usuario Put/Usuarios/{cedula}: Actualiza un usuario existente Delete/Usuarios/{cedula}: Elimina un usuario Ejemplo:

GET /Usuarios http://127.0.0.1:8000/Usuarios { "cedula": 1, "nombre": "Juan Pablo", "telefono": "4141234567", "correo": "Juan.Pablo1234@gmail.com" }, { "cedula": 2, "nombre": "Ana Torres", "telefono": "4147654321", "correo": "ana.torres@gmail.com" }

GET /Usuarios{cedula} http://127.0.0.1:8000/Usuarios/1 { "cedula": 1, "nombre": "Juan Pablo", "telefono": "4141234567", "correo": "Juan.Pablo1234@gmail.com" }

POST /Usuarios/ { "cedula": 3, "nombre": "Carlos Mendoza", "telefono": "4149876543", "correo": "carlos.mendoza@gmail.com" }

PUT /Usuarios/{cedula} Cambio de la cedula 3 --> 4 { "cedula": 4, "nombre": "Carlos Mendoza", "telefono": "4149876543", "correo": "carlos.mendoza@gmail.com" }

DELETE/Usuarios/{cedula} Eliminamos cedula 2 de la lista { "cedula": 1, "nombre": "Juan Pablo", "telefono": "4141234567", "correo": "Juan.Pablo1234@gmail.com" }, { "cedula": 4, "nombre": "Carlos Mendoza", "telefono": "4149876543", "correo": "carlos.mendoza@gmail.com" }

--Queda toda la informacion Actualizada--
Libros: Get/Libros: Listar libros Get/Libros/{Titulo}: Consulta un Libro por Titulo Post/Libros: Agregar libro Put/Libros/{Titulo}: Actualizar libro Delete/Libros/{Titulo}: Eliminar libro Ejemplo:

GET /Libros http://127.0.0.1:8000/Libros { "Titulo": "Cien años de soledad", "Autor": "Gabriel García Márquez", "Año": 1967, "Precio": 50000 }, { "Titulo": "Las crónicas de Dayron Moreno", "Autor": "Santiago Hernández", "Año": 2000, "Precio": 5000 }

GET /Libros/{Titulo} http://127.0.0.1:8000/Libros/Cien años de soledad { "Titulo": "Cien años de soledad", "Autor": "Gabriel García Márquez", "Año": 1967, "Precio": 50000 }

POST /Libros/ { "Titulo": "El amor en los tiempos del cólera", "Autor": "Gabriel García Márquez", "Año": 1985, "Precio": 45000 }

PUT /Libros/{Titulo} Cambio el titulo "Cien años de soledad" --> "La liga de la justicia" { "Titulo": "La liga de la justicia", "Autor": "G. García Márquez", "Año": 1967, "Precio": 50000 }

DELETE/Libros/{Titulo} Eliminamos el libro de titulo "El amor en los tiempos del cólera" { "Titulo": "La liga de la justicia", "Autor": "G. García Márquez", "Año": 1967, "Precio": 50000 }, { "Titulo": "Las crónicas de Dayron Moreno", "Autor": "Santiago Hernández", "Año": 2000, "Precio": 5000 }

--Queda toda la informacion Actualizada--
Prestamos: Get/Prestamos: Lista Prestamos Get/Prestamos/{idPrestamo}: Lista Prestamos por ID Post/Prestamos: Agrega Prestamo Put/Prestamos/{idPrestamo}: Actualiza Prestamo Delete/Prestamos/{idPrestamo}: Elimina Prestamo Ejemplo:

GET /Prestamos http://127.0.0.1:8000/Prestamos { "idPrestamo": 1, "cedulaUsuario": 1, "idLibro": 1001, "fechaPrestamo": "2025-09-05", "fechaDevolucion": null, "estadoPrestamo": "Activo" }, { "idPrestamo": 2, "cedulaUsuario": 2, "idLibro": 1001, "fechaPrestamo": "2025-08-05", "fechaDevolucion": "2025-09-05", "estadoPrestamo": "Devuelto" }

GET /Prestamos/{idPrestamo} http://127.0.0.1:8000/Prestamos/2 { "idPrestamo": 2, "cedulaUsuario": 2, "idLibro": 1001, "fechaPrestamo": "2025-08-05", "fechaDevolucion": "2025-09-05", "estadoPrestamo": "Devuelto" }

POST /Prestamos/ { "idPrestamo": 3, "cedulaUsuario": 1, "idLibro": 1002, "fechaPrestamo": "2025-09-06", "fechaDevolucion": null, "estadoPrestamo": "Activo" }

PUT /Prestamos/{idPrestamo} Cambio el idPrestamo 3 --> 4 { "idPrestamo": 4, "cedulaUsuario": 1, "idLibro": 1002, "fechaPrestamo": "2025-09-06", "fechaDevolucion": null, "estadoPrestamo": "Activo" }

DELETE/Prestamos/{idPrestamo} Eliminamos el prestamo que tiene de idPrestamo 1 { "idPrestamo": 2, "cedulaUsuario": 2, "idLibro": 1001, "fechaPrestamo": "2025-08-05", "fechaDevolucion": "2025-09-05", "estadoPrestamo": "Devuelto" }, { "idPrestamo": 4, "cedulaUsuario": 1, "idLibro": 1002, "fechaPrestamo": "2025-09-06", "fechaDevolucion": null, "estadoPrestamo": "Activo" }

--Queda toda la informacion Actualizada-- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------Integrantes:

Emanuel Valencia Marin
Juan Pablo Hernandez
Santiago Alvarez Alzate
