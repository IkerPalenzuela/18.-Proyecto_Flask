from app import db
from app.models.libro import Libro
from app.models.socio import Socio

# Listar libros
def listar_libros():
    return Libro.query.all()

# Listar solo disponibles
def listar_disponibles():
    # Usamos tu método 'socio_id' para filtrar
    return Libro.query.filter_by(socio_id=None).all()

# Buscar por título
def buscar_libros(termino):
    if not termino:
        return []
    return Libro.query.filter(Libro.titulo.ilike(f'%{termino}%')).all()

def obtener_libro(id):
    return Libro.query.get(id)

# Crear Libro
def crear_libro(titulo, autor, anio, categoria):
    libro = Libro(titulo=titulo, autor=autor, anio=anio, categoria=categoria)
    db.session.add(libro)
    db.session.commit()
    return libro

# Editar Libro
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

# Borrar Libro (Con validación)
def borrar_libro(id):
    libro = Libro.query.get(id)
    if not libro:
        return False, "El libro no existe."
    
    # Solo borrar si no está prestado
    if libro.socio_id is not None:
        return False, "No se puede borrar: El libro está prestado actualmente."

    try:
        db.session.delete(libro)
        db.session.commit()
        return True, "Libro eliminado correctamente."
    except:
        db.session.rollback()
        return False, "Error al eliminar libro."

# Prestar Libro
def prestar_libro(libro_id, socio_id):
    libro = Libro.query.get(libro_id)
    socio = Socio.query.get(socio_id)

    if not libro: return False, "El libro no existe."
    if not socio: return False, "El socio no existe."
    if libro.socio_id is not None:
        return False, "El libro ya está prestado."

    libro.socio_id = socio.id
    db.session.commit()
    return True, "Préstamo realizado con éxito."

# Devolver Libro
def devolver_libro(libro_id):
    libro = Libro.query.get(libro_id)
    
    if not libro or libro.socio_id is None:
        return False, "El libro no estaba prestado."
    
    libro.socio_id = None
    db.session.commit()
    return True, "Libro devuelto correctamente."