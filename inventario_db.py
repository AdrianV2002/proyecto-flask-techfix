import sqlite3

class Producto:
    def __init__(self, id_prod, nombre, cantidad, precio, descripcion, imagen):
        self._id_prod = id_prod
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio
        self._descripcion = descripcion
        self._imagen = imagen

    def get_id(self): return self._id_prod
    def get_nombre(self): return self._nombre
    def get_cantidad(self): return self._cantidad
    def get_precio(self): return self._precio
    def get_descripcion(self): return self._descripcion
    def get_imagen(self): return self._imagen

    def to_dict(self):
        return {
            "id": self._id_prod,
            "nombre": self._nombre,
            "cantidad": self._cantidad,
            "precio": self._precio,
            "descripcion": self._descripcion,
            "imagen": self._imagen
        }

class Inventario:
    def __init__(self, db_name="techfix.db"):
        self.db_name = db_name
        self.crear_tabla()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def crear_tabla(self):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                descripcion TEXT,
                imagen TEXT
            )
        ''')
        conexion.commit()
        conexion.close()

    def añadir_producto(self, nombre, cantidad, precio, descripcion, imagen):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO productos (nombre, cantidad, precio, descripcion, imagen) VALUES (?, ?, ?, ?, ?)", 
                       (nombre, cantidad, precio, descripcion, imagen))
        conexion.commit()
        conexion.close()

    def mostrar_productos(self):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos")
        filas = cursor.fetchall() 
        conexion.close()
        
        inventario_dict = {}
        for fila in filas:
            prod = Producto(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5])
            inventario_dict[prod.get_id()] = prod.to_dict()
            
        return list(inventario_dict.values())

    def actualizar_producto(self, id_prod, cantidad, precio):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?", 
                       (cantidad, precio, id_prod))
        conexion.commit()
        conexion.close()

    def eliminar_producto(self, id_prod):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id = ?", (id_prod,))
        conexion.commit()
        conexion.close()
        
    def buscar_producto(self, nombre_buscado):
        conexion = self.conectar()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre_buscado + '%',))
        filas = cursor.fetchall()
        conexion.close()
        
        inventario_dict = {}
        for fila in filas:
            prod = Producto(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5])
            inventario_dict[prod.get_id()] = prod.to_dict()
            
        return list(inventario_dict.values())