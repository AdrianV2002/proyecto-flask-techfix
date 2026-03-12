from flask import Flask, render_template, request, redirect, url_for
import random
import os

from inventario.bd import db
from inventario.productos import Producto
from inventario.inventario import sincronizar_respaldos, leer_archivos

# ==========================================
# IMPORTACIÓN NUEVA (SEMANA 13)
# Conector a nuestra base de datos MySQL
# ==========================================
from Conexion.conexion import obtener_conexion, inicializar_base_datos

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'techfix.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Inicializamos las tablas de MySQL si no existen
inicializar_base_datos()

def actualizar_archivos_respaldo():
    todos_los_productos = Producto.query.all()
    lista_dicts = [p.to_dict() for p in todos_los_productos]
    sincronizar_respaldos(lista_dicts)

@app.route('/')
def home():
    equipos = ['PC-GAMER', 'LAPTOP', 'MACBOOK', 'IMPRESORA', 'CELULAR']
    codigo_generado = f"{random.choice(equipos)}-{random.randint(100, 999)}"
    return render_template('index.html', ticket_aleatorio=codigo_generado)

@app.route('/ticket/<codigo>')
def consultar_ticket(codigo):
    return render_template('ticket.html', codigo=codigo)

@app.route('/about')
def about(): 
    return render_template('about.html')

@app.route('/servicios')
def servicios():
    lista_servicios = [
        {"nombre": "Mantenimiento Preventivo", "tiempo": "2 horas", "precio": 35.00},
        {"nombre": "Instalación de Sistema Operativo", "tiempo": "1 hora", "precio": 25.00},
        {"nombre": "Limpieza de Hardware", "tiempo": "3 horas", "precio": 45.00}
    ]
    return render_template('servicios.html', servicios=lista_servicios)

# ==========================================
# RUTAS MYSQL - GESTIÓN DE USUARIOS
# Operaciones: Leer, Insertar, Actualizar, Eliminar
# ==========================================
@app.route('/usuarios')
def lista_usuarios():
    conn = obtener_conexion()
    if not conn:
        return "Error: No hay conexión a MySQL. Revisa tu panel XAMPP/WAMP.", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios_db)

@app.route('/agregar_usuario', methods=['POST'])
def agregar_usuario():
    nombre = request.form.get('nombre')
    mail = request.form.get('mail')
    password = request.form.get('password')
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre, mail, password))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('lista_usuarios'))

@app.route('/actualizar_usuario', methods=['POST'])
def actualizar_usuario():
    id_usuario = int(request.form.get('id_usuario'))
    nombre = request.form.get('nombre')
    mail = request.form.get('mail')
    password = request.form.get('password')
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor()
        sql = "UPDATE usuarios SET nombre = %s, mail = %s, password = %s WHERE id_usuario = %s"
        cursor.execute(sql, (nombre, mail, password, id_usuario))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('lista_usuarios'))

@app.route('/eliminar_usuario/<int:id_usuario>')
def eliminar_usuario(id_usuario):
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor()
        sql = "DELETE FROM usuarios WHERE id_usuario = %s"
        cursor.execute(sql, (id_usuario,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('lista_usuarios'))

# ==========================================
# RUTAS MYSQL - GESTIÓN DE CLIENTES
# Reemplaza la lista estática anterior por conexión a DB
# ==========================================
@app.route('/clientes')
def clientes():
    conn = obtener_conexion()
    if not conn:
        return "Error: No hay conexión a MySQL. Revisa tu panel XAMPP/WAMP.", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    clientes_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('clientes.html', clientes=clientes_db)

@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    nombre = request.form.get('nombre')
    equipo = request.form.get('equipo')
    estado = request.form.get('estado')
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor()
        sql = "INSERT INTO clientes (nombre, equipo, estado) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre, equipo, estado))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('clientes'))

@app.route('/actualizar_cliente', methods=['POST'])
def actualizar_cliente():
    id_cliente = int(request.form.get('id_cliente'))
    nombre = request.form.get('nombre')
    equipo = request.form.get('equipo')
    estado = request.form.get('estado')
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor()
        sql = "UPDATE clientes SET nombre = %s, equipo = %s, estado = %s WHERE id_cliente = %s"
        cursor.execute(sql, (nombre, equipo, estado, id_cliente))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('clientes'))

@app.route('/eliminar_cliente/<int:id_cliente>')
def eliminar_cliente(id_cliente):
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor()
        sql = "DELETE FROM clientes WHERE id_cliente = %s"
        cursor.execute(sql, (id_cliente,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('clientes'))

@app.route('/inventario')
def inventario():
    query = request.args.get('q')
    if query:
        productos = Producto.query.filter(Producto.nombre.ilike(f'%{query}%')).all()
    else:
        productos = Producto.query.all()
    return render_template('inventario.html', productos=productos)

@app.route('/catalogo')
def catalogo():
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)

@app.route('/agregar', methods=['POST'])
def agregar():
    nuevo_producto = Producto(
        nombre=request.form.get('nombre'),
        cantidad=int(request.form.get('cantidad')),
        precio=float(request.form.get('precio')),
        descripcion=request.form.get('descripcion'),
        imagen=request.form.get('imagen')
    )
    db.session.add(nuevo_producto)
    db.session.commit()
    actualizar_archivos_respaldo()
    return redirect(url_for('inventario'))

@app.route('/eliminar/<int:id_prod>')
def eliminar(id_prod):
    producto = Producto.query.get_or_404(id_prod)
    db.session.delete(producto)
    db.session.commit()
    actualizar_archivos_respaldo()
    return redirect(url_for('inventario'))

@app.route('/actualizar', methods=['POST'])
def actualizar():
    id_prod = int(request.form.get('id_prod'))
    producto = Producto.query.get_or_404(id_prod)
    producto.cantidad = int(request.form.get('cantidad'))
    producto.precio = float(request.form.get('precio'))
    db.session.commit()
    actualizar_archivos_respaldo()
    return redirect(url_for('inventario'))

@app.route('/datos')
def datos():
    data = leer_archivos()
    productos_db = Producto.query.all()
    return render_template('datos.html', 
                           productos_db=productos_db,
                           datos_txt=data['txt'], 
                           datos_json=data['json'], 
                           datos_csv=data['csv'])

if __name__ == '__main__':
    app.run(debug=True)