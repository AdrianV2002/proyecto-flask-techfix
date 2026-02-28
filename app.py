from flask import Flask, render_template, request, redirect, url_for
import random
from inventario_db import Inventario

app = Flask(__name__)

mi_inventario = Inventario()

@app.route('/')
def home():
    equipos = ['PC-GAMER', 'LAPTOP', 'MACBOOK', 'IMPRESORA', 'CELULAR']
    numero = random.randint(100, 999)
    codigo_generado = f"{random.choice(equipos)}-{numero}"
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
        productos = mi_inventario.buscar_producto(query)
    else:
        productos = mi_inventario.mostrar_productos()
        
    return render_template('inventario.html', productos=productos)

@app.route('/catalogo')
def catalogo():
    productos = mi_inventario.mostrar_productos()
    return render_template('productos.html', productos=productos)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form.get('nombre')
    cantidad = int(request.form.get('cantidad'))
    precio = float(request.form.get('precio'))
    descripcion = request.form.get('descripcion')
    imagen = request.form.get('imagen')
    
    mi_inventario.añadir_producto(nombre, cantidad, precio, descripcion, imagen)
    return redirect(url_for('inventario'))

@app.route('/eliminar/<int:id_prod>')
def eliminar(id_prod):
    mi_inventario.eliminar_producto(id_prod)
    return redirect(url_for('inventario'))

@app.route('/actualizar', methods=['POST'])
def actualizar():
    id_prod = int(request.form.get('id_prod'))
    cantidad = int(request.form.get('cantidad'))
    precio = float(request.form.get('precio'))
    mi_inventario.actualizar_producto(id_prod, cantidad, precio)
    return redirect(url_for('inventario'))

if __name__ == '__main__':
    app.run(debug=True)