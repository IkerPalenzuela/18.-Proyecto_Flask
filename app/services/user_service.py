from app import db
from app.models.user import User
from flask import session
from werkzeug.security import generate_password_hash

class UserService:
    @staticmethod
    def authenticate(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None
    
    @staticmethod
    def ensure_admin():
        admin = User.query.filter_by(username="admin").first() 
        if not admin:
            admin = User(
                username="admin", 
                nombre="Administrador",
                email="admin@admin.com",
                role="admin"
            )
            admin.set_password("admin") 
            db.session.add(admin)
            db.session.commit()
            print("Admin creado")
        return admin
    
    @staticmethod
    def crear_socios_ejemplo():
        if User.query.count() <= 1:
            socio1 = User(username="juan", nombre="Juan Pérez", email="juan@email.com", role="user")
            socio1.set_password("1234")
            db.session.add(socio1)
            
            socio2 = User(username="maria", nombre="María García", email="maria@email.com", role="user")
            socio2.set_password("1234")
            db.session.add(socio2)
            
            db.session.commit()
            print("Socios de ejemplo creados")

    @staticmethod
    def get_all_socios():
        return User.query.all()

    @staticmethod
    def get_socio_by_id(id):
        return User.query.get(id)

    @staticmethod
    def crear_socio(nombre, email, username=None, password=None):
        if not username:
            username = email.split('@')[0]
        
        if User.query.filter((User.email == email) | (User.username == username)).first():
            return False, "El usuario o email ya existe."

        nuevo_socio = User(
            username=username, 
            nombre=nombre, 
            email=email, 
            role="user"
        )
        
        if password:
            nuevo_socio.set_password(password)
        else:
            nuevo_socio.set_password("1234")

        try:
            db.session.add(nuevo_socio)
            db.session.commit()
            return True, "Socio creado correctamente."
        except Exception as e:
            db.session.rollback()
            return False, f"Error al guardar en base de datos: {str(e)}"

    @staticmethod
    def editar_socio(id, nombre, email):
        user = User.query.get(id)
        if not user:
            return False, "Usuario no encontrado"
        
        user.nombre = nombre
        user.email = email
        
        try:
            db.session.commit()
            return True, "Socio actualizado correctamente."
        except Exception as e:
            db.session.rollback()
            return False, "Error al actualizar."

    @staticmethod
    def borrar_socio(id):
        user = User.query.get(id)
        if not user:
            return False, "Usuario no encontrado"
        
        if user.libros: 
            return False, "No se puede borrar: El socio tiene libros sin devolver."

        try:
            db.session.delete(user)
            db.session.commit()
            return True, "Socio eliminado correctamente."
        except Exception as e:
            return False, "Error al eliminar."

    @staticmethod
    def get_socios_con_prestamo():
        return User.query.filter(User.libros.any()).all()

    @staticmethod
    def get_socios_disponibles():
        return User.query.filter(~User.libros.any()).all()