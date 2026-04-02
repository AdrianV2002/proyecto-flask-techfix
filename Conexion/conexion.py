import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    try:
        conexion = mysql.connector.connect(
            host="163.227.179.114",
            user="u214192_tAzwp1v4Im",
            password="t9JOALW0f!XbXjZp+^o.5GS3",
            database="s214192_techfix_db"
        )
        if conexion.is_connected():
            return conexion
    except Error:
        return None

def inicializar_base_datos():
    conn = obtener_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                    cedula VARCHAR(20) NOT NULL,
                    nombre VARCHAR(100) NOT NULL,
                    telefono VARCHAR(20) NOT NULL,
                    direccion TEXT NOT NULL,
                    mail VARCHAR(100) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    rol VARCHAR(20) DEFAULT 'usuario'
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tickets (
                    id_ticket INT AUTO_INCREMENT PRIMARY KEY,
                    id_usuario INT NOT NULL,
                    equipo VARCHAR(100) NOT NULL,
                    descripcion TEXT NOT NULL,
                    estado VARCHAR(20) DEFAULT 'Pendiente',
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mensajes_ticket (
                    id_mensaje INT AUTO_INCREMENT PRIMARY KEY,
                    id_ticket INT NOT NULL,
                    id_usuario INT NOT NULL,
                    mensaje TEXT NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_ticket) REFERENCES tickets(id_ticket) ON DELETE CASCADE,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(150) NOT NULL,
                    cantidad INT NOT NULL,
                    precio DECIMAL(10,2) NOT NULL,
                    descripcion TEXT NOT NULL,
                    imagen VARCHAR(255) NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS compras (
                    id_compra INT AUTO_INCREMENT PRIMARY KEY,
                    id_usuario INT NOT NULL,
                    producto VARCHAR(150) NOT NULL,
                    precio DECIMAL(10,2) NOT NULL,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) ON DELETE CASCADE
                )
            """)
            conn.commit()
            cursor.close()
        except Error:
            pass
        finally:
            conn.close()