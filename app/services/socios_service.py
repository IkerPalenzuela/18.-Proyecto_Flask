from app import db
from app.models.socio import Socio

# Listar todos
def listar_todos():
    return Socio.query.all()

# Obtener uno por ID
def obtener_por_id(id):
    return Socio.query.get(id)

# Crear Socio
def crear_socio(nombre, email):
    # Validamos que el email no exista ya
    if Socio.query.filter_by(email=email).first():
        return False, "Ese email ya está registrado."

    nuevo_socio = Socio(nombre=nombre, email=email)
    
    try:
        db.session.add(nuevo_socio)
        db.session.commit()
        return True, "Socio creado correctamente."
    except Exception as e:
        db.session.rollback()
        return False, "Error al guardar en base de datos."

# Editar Socio
def editar_socio(id, nombre, email):
    socio = Socio.query.get(id)
    if not socio:
        return False, "Socio no encontrado"
    
    # Comprobamos que el email nuevo no sea de otra persona
    socio_existente = Socio.query.filter_by(email=email).first()
    if socio_existente and socio_existente.id != id:
        return False, "Ese email ya pertenece a otro socio."

    socio.nombre = nombre
    socio.email = email
    
    try:
        db.session.commit()
        return True, "Socio actualizado correctamente."
    except:
        db.session.rollback()
        return False, "Error al actualizar."

# Borrar Socio
def borrar_socio(id):
    socio = Socio.query.get(id)
    if not socio:
        return False, "Socio no encontrado"
    
    if socio.libros: 
        return False, "No se puede borrar: El socio tiene libros sin devolver."

    try:
        db.session.delete(socio)
        db.session.commit()
        return True, "Socio eliminado correctamente."
    except:
        db.session.rollback()
        return False, "Error al eliminar."

# API: Listado de préstamos
def obtener_listado_prestamos_api():
    socios = Socio.query.filter(Socio.libros.any()).all()
    resultado = []
    
    for socio in socios:
        for libro in socio.libros:
            resultado.append({
                "socio_id": socio.id,
                "socio_nombre": socio.nombre,
                "socio_email": socio.email,
                "libro_id": libro.id,
                "libro_titulo": libro.titulo,
                "libro_autor": libro.autor
            })
    return resultado

# Funcion para crear socios
def seed_socios():
    if Socio.query.count() == 0:
        datos = [
            ("Iker Casillas", "iker@mail.com"), ("Maria Garcia", "maria@mail.com"),
            ("Juan Perez", "juan@mail.com"), ("Ana Belen", "ana@mail.com"),
            ("Carlos Sainz", "carlos@mail.com"), ("Elena Furiase", "elena@mail.com"),
            ("David Bisbal", "david@mail.com"), ("Lucia Gil", "lucia@mail.com"),
            ("Sergio Ramos", "sergio@mail.com"), ("Paula Echevarria", "paula@mail.com"),
            ("Fernando Alonso", "fernando@mail.com"), ("Sara Carbonero", "sara@mail.com"),
            ("Jordi Alta", "jordi@mail.com"), ("Marta Sanchez", "marta@mail.com"),
            ("Roberto Canario", "roberto@mail.com")
        ]
        for nombre, email in datos:
            nuevo = Socio(nombre=nombre, email=email)
            db.session.add(nuevo)
        db.session.commit()
        print("15 Socios creados.")