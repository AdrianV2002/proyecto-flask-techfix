import mysql.connector
from mysql.connector import Error

def obtener_conexion():
    """Establece y retorna la conexión a la base de datos MySQL"""
    try:
        conexion = mysql.connector.connect(
            host="163.227.179.114",
            user="u214192_tAzwp1v4Im",
            password="t9JOALW0f!XbXjZp+^o.5GS3",
            database="s214192_techfix_db"
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error crítico al conectar a MySQL: {e}")
        return None

def inicializar_base_datos():
    """Crea las tablas en MySQL automáticamente si no existen"""
    conn = obtener_conexion()
    if conn:
        try:
            cursor = conn.cursor()
            
            # 1. Crear tabla de usuarios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    mail VARCHAR(100) NOT NULL,
                    password VARCHAR(255) NOT NULL
                )
            """)
            
            # 2. Crear tabla de clientes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    equipo VARCHAR(100) NOT NULL,
                    estado VARCHAR(50) NOT NULL
                )
            """)
            
            conn.commit()
            cursor.close()
            print("Tablas de MySQL verificadas y listas para usar.")
        except Error as e:
            print(f"Error al crear las tablas: {e}")
        finally:
            conn.close()