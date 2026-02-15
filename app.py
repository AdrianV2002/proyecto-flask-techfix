from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <div style="text-align: center;">
        <h1>Bienvenido a TechFix</h1>
        <h3>Sistema de Gestión de Reparaciones y Soporte Técnico</h3>
        <p>Consulta el estado de tus equipos y gestiona tus turnos aquí.</p>
    </div>
    """

@app.route('/ticket/<codigo>')
def consultar_ticket(codigo):
    return f"""
    <h2>📄 Consulta de Ticket</h2>
    <p>El equipo asociado al ticket <b>{codigo}</b> ha sido recibido correctamente.</p>
    <p>Estado actual: <span style="color: green;">En Diagnóstico Técnico</span></p>
    """

if __name__ == '__main__':
    app.run(debug=True)