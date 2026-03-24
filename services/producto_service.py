from Conexion.conexion import obtener_conexion

class ProductoService:
    @staticmethod
    def obtener_todos(busqueda=None):
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)
        if busqueda:
            cursor.execute("SELECT * FROM productos WHERE nombre LIKE %s", (f"%{busqueda}%",))
        else:
            cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        cursor.close()
        conn.close()
        return productos

    @staticmethod
    def crear(datos):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, cantidad, precio, descripcion, imagen) VALUES (%s, %s, %s, %s, %s)", 
                       (datos['nombre'], datos['cantidad'], datos['precio'], datos['descripcion'], datos['imagen']))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def actualizar(id_prod, datos):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("UPDATE productos SET cantidad = %s, precio = %s WHERE id = %s", 
                       (datos['cantidad'], datos['precio'], id_prod))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def eliminar(id_prod):
        conn = obtener_conexion()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (id_prod,))
        conn.commit()
        cursor.close()
        conn.close()