from flask import Flask, render_template, request, redirect, url_for, flash, abort
import os
from inventario.inventario import sincronizar_respaldos, leer_archivos
from Conexion.conexion import obtener_conexion, inicializar_base_datos
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from inventario.models import Usuario

app = Flask(__name__)
app.secret_key = 'clave_secreta_2026'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Inicia sesión para interactuar.'

inicializar_base_datos()

def crear_admin_por_defecto():
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE mail = 'admin@admin.com'")
        if not cursor.fetchone():
            password_hash = generate_password_hash('admin')
            sql = "INSERT INTO usuarios (nombre, mail, password, rol) VALUES ('Administrador', 'admin@admin.com', %s, 'admin')"
            cursor.execute(sql, (password_hash,))
            conn.commit()
        cursor.close()
        conn.close()

crear_admin_por_defecto()

def actualizar_archivos_respaldo():
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()
        for p in productos:
            p['precio'] = float(p['precio'])
        sincronizar_respaldos(productos)
        cursor.close()
        conn.close()

@login_manager.user_loader
def load_user(user_id):
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        if data:
            return Usuario(data['id_usuario'], data['nombre'], data['mail'], data['password'], data['rol'])
    return None

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        mail = request.form.get('mail')
        password_hash = generate_password_hash(request.form.get('password'))
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, mail, password, rol) VALUES (%s, %s, %s, 'usuario')", (nombre, mail, password_hash))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form.get('mail')
        password = request.form.get('password')
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE mail = %s", (mail,))
            data = cursor.fetchone()
            cursor.close()
            conn.close()
            if data and check_password_hash(data['password'], password):
                user = Usuario(data['id_usuario'], data['nombre'], data['mail'], data['password'], data['rol'])
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash("Credenciales incorrectas", "danger")
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('productos.html', productos=productos)

@app.route('/servicios')
def servicios():
    lista_servicios = [
        {"nombre": "Mantenimiento Preventivo", "tiempo": "2 horas", "precio": 35.00},
        {"nombre": "Instalación de Sistema Operativo", "tiempo": "1 hora", "precio": 25.00},
        {"nombre": "Limpieza de Hardware", "tiempo": "3 horas", "precio": 45.00}
    ]
    return render_template('servicios.html', servicios=lista_servicios)

@app.route('/soporte', methods=['GET', 'POST'])
@login_required
def soporte():
    servicio_pre = request.args.get('servicio', '')
    if request.method == 'POST':
        equipo = request.form.get('equipo')
        descripcion = request.form.get('descripcion')
        conn = obtener_conexion()
        if conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tickets (id_usuario, equipo, descripcion, estado) VALUES (%s, %s, %s, 'Pendiente')", 
                           (current_user.id, equipo, descripcion))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Ticket generado con éxito.", "success")
            return redirect(url_for('mis_tickets'))
    return render_template('soporte.html', servicio_pre=servicio_pre)

@app.route('/mis_tickets')
@login_required
def mis_tickets():
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor(dictionary=True)
        if current_user.rol == 'admin':
            cursor.execute("SELECT t.*, u.nombre, u.mail FROM tickets t JOIN usuarios u ON t.id_usuario = u.id_usuario ORDER BY t.fecha DESC")
        else:
            cursor.execute("SELECT * FROM tickets WHERE id_usuario = %s ORDER BY fecha DESC", (current_user.id,))
        tickets = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('tickets.html', tickets=tickets)
    return abort(500)

@app.route('/ticket/<int:id_ticket>', methods=['GET', 'POST'])
@login_required
def detalle_ticket(id_ticket):
    conn = obtener_conexion()
    if not conn: abort(500)
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        mensaje = request.form.get('mensaje')
        if mensaje:
            cursor.execute("INSERT INTO mensajes_ticket (id_ticket, id_usuario, mensaje) VALUES (%s, %s, %s)", 
                           (id_ticket, current_user.id, mensaje))
            conn.commit()
        
        nuevo_estado = request.form.get('estado')
        if nuevo_estado and current_user.rol == 'admin':
            cursor.execute("UPDATE tickets SET estado = %s WHERE id_ticket = %s", (nuevo_estado, id_ticket))
            conn.commit()
        return redirect(url_for('detalle_ticket', id_ticket=id_ticket))

    cursor.execute("SELECT t.*, u.nombre, u.mail FROM tickets t JOIN usuarios u ON t.id_usuario = u.id_usuario WHERE t.id_ticket = %s", (id_ticket,))
    ticket = cursor.fetchone()
    
    if not ticket or (current_user.rol != 'admin' and ticket['id_usuario'] != current_user.id):
        abort(403)
        
    cursor.execute("SELECT m.*, u.nombre, u.rol FROM mensajes_ticket m JOIN usuarios u ON m.id_usuario = u.id_usuario WHERE m.id_ticket = %s ORDER BY m.fecha ASC", (id_ticket,))
    mensajes = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('ticket_detalle.html', ticket=ticket, mensajes=mensajes)

@app.route('/usuarios')
@login_required
def lista_usuarios():
    if current_user.rol != 'admin': abort(403)
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT u.*, (SELECT COUNT(*) FROM tickets t WHERE t.id_usuario = u.id_usuario) as total_tickets 
        FROM usuarios u
    """)
    usuarios_db = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('usuarios.html', usuarios=usuarios_db)

@app.route('/cambiar_rol', methods=['POST'])
@login_required
def cambiar_rol():
    if current_user.rol != 'admin': abort(403)
    id_usuario = request.form.get('id_usuario')
    nuevo_rol = request.form.get('rol')
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE usuarios SET rol = %s WHERE id_usuario = %s", (nuevo_rol, id_usuario))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('lista_usuarios'))

@app.route('/eliminar_usuario/<int:id_usuario>')
@login_required
def eliminar_usuario(id_usuario):
    if current_user.rol != 'admin': abort(403)
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        conn.commit()
        cursor.close()
        conn.close()
    return redirect(url_for('lista_usuarios'))

@app.route('/inventario')
@login_required
def inventario():
    if current_user.rol != 'admin': abort(403)
    query = request.args.get('q')
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    if query:
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE %s", (f"%{query}%",))
    else:
        cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('inventario.html', productos=productos)

@app.route('/agregar', methods=['POST'])
@login_required
def agregar():
    if current_user.rol != 'admin': abort(403)
    nombre = request.form.get('nombre')
    cantidad = int(request.form.get('cantidad'))
    precio = float(request.form.get('precio'))
    descripcion = request.form.get('descripcion')
    imagen = request.form.get('imagen')
    
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, cantidad, precio, descripcion, imagen) VALUES (%s, %s, %s, %s, %s)", 
                       (nombre, cantidad, precio, descripcion, imagen))
        conn.commit()
        cursor.close()
        conn.close()
        actualizar_archivos_respaldo()
    return redirect(url_for('inventario'))

@app.route('/actualizar', methods=['POST'])
@login_required
def actualizar():
    if current_user.rol != 'admin': abort(403)
    id_prod = int(request.form.get('id_prod'))
    cantidad = int(request.form.get('cantidad'))
    precio = float(request.form.get('precio'))
    
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE productos SET cantidad = %s, precio = %s WHERE id = %s", (cantidad, precio, id_prod))
        conn.commit()
        cursor.close()
        conn.close()
        actualizar_archivos_respaldo()
    return redirect(url_for('inventario'))

@app.route('/eliminar/<int:id_prod>')
@login_required
def eliminar(id_prod):
    if current_user.rol != 'admin': abort(403)
    conn = obtener_conexion()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM productos WHERE id = %s", (id_prod,))
        conn.commit()
        cursor.close()
        conn.close()
        actualizar_archivos_respaldo()
    return redirect(url_for('inventario'))

@app.route('/datos')
@login_required
def datos():
    if current_user.rol != 'admin': abort(403)
    conn = obtener_conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos")
    productos_db = cursor.fetchall()
    cursor.close()
    conn.close()
    
    data = leer_archivos()
    return render_template('datos.html', productos_db=productos_db, datos_txt=data['txt'], datos_json=data['json'], datos_csv=data['csv'])

@app.errorhandler(403)
def acceso_denegado(error):
    return render_template('403.html'), 403

if __name__ == '__main__':
    app.run(debug=True)