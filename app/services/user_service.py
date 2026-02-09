from app import db
from app.models.user import Usuario

class UserService:
    # Valida el login del Administrador
    @staticmethod
    def authenticate(username, password):
        # Buscamos por username en la tabla 'usuarios'
        user = Usuario.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None
    
    # Crea un admin por defecto si no existe
    @staticmethod
    def ensure_admin():
        admin = Usuario.query.filter_by(username="admin").first() 
        if not admin:
            # Creamos el usuario con los campos de tu modelo Usuario
            admin = Usuario(username="admin", rol="admin")
            admin.set_password("admin") 
            db.session.add(admin)
            db.session.commit()
            print("--- Admin creado (User: admin / Pass: admin) ---")
        return admin