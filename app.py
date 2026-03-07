from flask import Flask, render_template, request, redirect, url_for
import random
import os

# Importaciones de nuestra nueva estructura modular
from inventario.bd import db
from inventario.productos import Producto
# ¡Corregido! Una sola importación con los nombres correctos
from inventario.inventario import sincronizar_respaldos, leer_archivos

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'techfix.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar la base de datos con la app
db.init_app(app)

# Crear las tablas automáticamente si no existen
with app.app_context():
    db.create_all()

def actualizar_archivos_respaldo():
    """Lee toda la base de datos y manda a actualizar los 3 archivos"""
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

@app.route('/clientes')
def clientes():
    lista_clientes = [
        {"nombre": "Empresa ABC", "equipo": "Servidor Dell", "estado": "VIP"},
        {"nombre": "Carlos Mendoza", "equipo": "PC Gamer", "estado": "Regular"},
        {"nombre": "Ana Torres", "equipo": "MacBook Air", "estado": "Nuevo"}
    ]
    return render_template('clientes.html', clientes=lista_clientes)

@app.route('/inventario')
def inventario():
    query = request.args.get('q')
    if query:
        # Búsqueda con SQLAlchemy
        productos = Producto.query.filter(Producto.nombre.ilike(f'%{query}%')).all()
    else:
        # Mostrar todo con SQLAlchemy
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
    
    # ¡Sincronizamos archivos al agregar!
    actualizar_archivos_respaldo()
    return redirect(url_for('inventario'))

@app.route('/eliminar/<int:id_prod>')
def eliminar(id_prod):
    producto = Producto.query.get_or_404(id_prod)
    db.session.delete(producto)
    db.session.commit()
    
    # ¡Sincronizamos archivos al eliminar!
    actualizar_archivos_respaldo()
    return redirect(url_for('inventario'))

@app.route('/actualizar', methods=['POST'])
def actualizar():
    id_prod = int(request.form.get('id_prod'))
    producto = Producto.query.get_or_404(id_prod)
    producto.cantidad = int(request.form.get('cantidad'))
    producto.precio = float(request.form.get('precio'))
    db.session.commit()
    
    # ¡Sincronizamos archivos al actualizar!
    actualizar_archivos_respaldo()
    return redirect(url_for('inventario'))

# --- RUTA DE RESPALDOS (SEMANA 12) ---
@app.route('/datos')
def datos():
    data = leer_archivos()
    productos_db = Producto.query.all()
    # Enviamos los nombres exactos que espera nuestro datos.html
    return render_template('datos.html', 
                           productos_db=productos_db,
                           datos_txt=data['txt'], 
                           datos_json=data['json'], 
                           datos_csv=data['csv'])

if __name__ == '__main__':
    app.run(debug=True)