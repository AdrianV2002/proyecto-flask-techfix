from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id_usuario, cedula, nombre, telefono, direccion, mail, password, rol):
        self.id = id_usuario
        self.cedula = cedula
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
        self.mail = mail
        self.password = password
        self.rol = rol