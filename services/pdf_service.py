from fpdf import FPDF
from Conexion.conexion import obtener_conexion

class PDFReporte(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 210, 255) 
        self.cell(0, 10, 'TechFix - Reporte General del Sistema', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

class PDFService:
    @staticmethod
    def generar_reporte_general(filepath):
        pdf = PDFReporte()
        pdf.add_page()
        
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)

        pdf.set_font('Arial', 'B', 12)
        pdf.set_fill_color(30, 30, 30)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, ' 1. Registro de Usuarios y Casos de Soporte', 0, 1, 'L', True)
        pdf.ln(3)

        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()

        for u in usuarios:
            pdf.set_font('Arial', 'B', 10)
            pdf.set_text_color(0, 0, 0)
            rol_texto = "Administrador" if u['rol'] == 'admin' else "Cliente"
            pdf.cell(0, 8, f"Usuario: {u['nombre']} | Correo: {u['mail']} | Rol: {rol_texto}", 0, 1, 'L')

            cursor.execute("SELECT * FROM tickets WHERE id_usuario = %s", (u['id_usuario'],))
            tickets = cursor.fetchall()

            pdf.set_font('Arial', '', 9)
            if tickets:
                for t in tickets:
                    pdf.cell(10, 6, "", 0, 0)
                    pdf.cell(0, 6, f"- Ticket #{t['id_ticket']}: {t['equipo']} (Estado: {t['estado']})", 0, 1, 'L')
            else:
                pdf.cell(10, 6, "", 0, 0)
                pdf.set_text_color(120, 120, 120)
                pdf.cell(0, 6, "No ha solicitado tickets de soporte.", 0, 1, 'L')
                pdf.set_text_color(0, 0, 0)
            pdf.ln(2)

        pdf.ln(5)

        pdf.set_font('Arial', 'B', 12)
        pdf.set_fill_color(30, 30, 30)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, ' 2. Estado del Inventario (Repuestos)', 0, 1, 'L', True)
        pdf.ln(3)

        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        pdf.set_font('Arial', 'B', 10)
        pdf.set_fill_color(220, 220, 220)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(20, 8, 'ID', 1, 0, 'C', True)
        pdf.cell(100, 8, 'Producto', 1, 0, 'C', True)
        pdf.cell(30, 8, 'Stock', 1, 0, 'C', True)
        pdf.cell(40, 8, 'Precio ($)', 1, 1, 'C', True)

        pdf.set_font('Arial', '', 9)
        for p in productos:
            pdf.cell(20, 8, str(p['id']), 1, 0, 'C')
            pdf.cell(100, 8, p['nombre'][:45], 1, 0, 'L')
            pdf.cell(30, 8, str(p['cantidad']), 1, 0, 'C')
            pdf.cell(40, 8, f"{p['precio']:.2f}", 1, 1, 'C')

        cursor.close()
        conn.close()

        pdf.output(filepath)