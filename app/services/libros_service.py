from app import db
from app.models.libro import Libro
from app.models.user import User

def listar_libros():
    return Libro.query.all()

def listar_disponibles():
    return Libro.query.filter_by(socio_id=None).all()

def buscar_libros(termino):
    if not termino:
        return []
    return Libro.query.filter(Libro.titulo.ilike(f'%{termino}%')).all()

def obtener_libro(id):
    return Libro.query.get(id)

def crear_libro(titulo, autor, anio, categoria):
    libro = Libro(titulo=titulo, autor=autor, anio=anio, categoria=categoria)
    db.session.add(libro)
    db.session.commit()
    return libro

def editar_libro(libro_id, titulo=None, autor=None, anio=None, categoria=None):
    libro = Libro.query.get(libro_id)
    if not libro:
        return None

    if titulo: libro.titulo = titulo
    if autor: libro.autor = autor
    if anio: libro.anio = anio
    if categoria: libro.categoria = categoria
    
    db.session.commit()
    return libro

# Función para prestar un libro a un socio
def prestar_libro(libro_id, socio_id):
    libro = Libro.query.get(libro_id)
    socio = User.query.get(socio_id)

    if not libro:
        return False, "El libro no existe."
    
    if not socio:
        return False, "El socio no existe."
    
    # Comprobar si el libro está disponible
    if not libro.esta_disponible():
        return False, "El libro ya está prestado."

    # Comprobar si el socio ya tiene un libro
    if socio.libros:
        return False, "El socio ya tiene un libro prestado."

    libro.socio_id = socio.id
    db.session.commit()
    return True, "Préstamo realizado con éxito."

# Función para devolver un libro
def devolver_libro(libro_id):
    libro = Libro.query.get(libro_id)
    if not libro or libro.socio_id is None:
        return False, "El libro no estaba prestado."
    
    libro.socio_id = None
    db.session.commit()
    return True, "Libro devuelto correctamente."