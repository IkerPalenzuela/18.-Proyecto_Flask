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
    # Validamos que el email no este registrado
    if Socio.query.filter_by(email=email).first():
        return False, "Ese email ya está registrado."

    nuevo_socio = Socio(nombre=nombre, email=email)
    
    # Intentamos guardar el nuevo socio en la bd
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
    
    # Intentamos guardar los cambios en la bd
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

    # Intentamos eliminar el socio de la bd
    try:
        db.session.delete(socio)
        db.session.commit()
        return True, "Socio eliminado correctamente."
    except:
        db.session.rollback()
        return False, "Error al eliminar."

# API: Listado de préstamos
def obtener_listado_prestamos_api():
    # Filtramos los socios que tienen libros
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
            ("Antonio García", "antonio.garcia@mail.com"), ("Carmen López", "carmen.lopez@mail.com"),
            ("Manuel Rodríguez", "manuel.rodriguez@mail.com"), ("Laura Martínez", "laura.martinez@mail.com"),
            ("José González", "jose.gonzalez@mail.com"), ("Ana Fernández", "ana.fernandez@mail.com"),
            ("David Pérez", "david.perez@mail.com"), ("Isabel Sánchez", "isabel.sanchez@mail.com"),
            ("Javier Ruiz", "javier.ruiz@mail.com"), ("María Gómez", "maria.gomez@mail.com"),
            ("Francisco Díaz", "francisco.diaz@mail.com"), ("Elena Martín", "elena.martin@mail.com"),
            ("Pablo Jiménez", "pablo.jimenez@mail.com"), ("Raquel Moreno", "raquel.moreno@mail.com"),
            ("Álvaro Muñoz", "alvaro.munoz@mail.com")
        ]
        for nombre, email in datos:
            nuevo = Socio(nombre=nombre, email=email)
            db.session.add(nuevo)
        
        db.session.commit()
        print("15 Socios (datos realistas) creados.")