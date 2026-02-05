from app import db
from app.models.user import User

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
    def get_all_socios():
        return User.query.all()
    
    @staticmethod
    def crear_socios_ejemplo():
        # Solo crear si no hay socios (aparte del admin)
        if User.query.count() <= 1:
            # Socio 1
            socio1 = User(
                username="juan",
                nombre="Juan Pérez",
                email="juan@email.com",
                role="user"
            )
            socio1.set_password("1234")
            db.session.add(socio1)
            
            # Socio 2
            socio2 = User(
                username="maria",
                nombre="María García",
                email="maria@email.com",
                role="user"
            )
            socio2.set_password("1234")
            db.session.add(socio2)
            
            db.session.commit()
            print("Socios de ejemplo creados")