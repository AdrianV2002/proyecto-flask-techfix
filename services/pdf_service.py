from fpdf import FPDF
from Conexion.conexion import obtener_conexion
from datetime import datetime

class PDFReporte(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 22)
        self.set_text_color(30, 30, 30)
        self.cell(100, 10, 'TECHFIX', 0, 0, 'L')
        
        self.set_font('Arial', '', 10)
        self.set_text_color(100, 100, 100)
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cell(0, 10, f'Emision: {fecha_actual}', 0, 1, 'R')
        
        self.set_font('Arial', 'I', 11)
        self.set_text_color(0, 210, 255)
        self.cell(0, 6, 'Reporte Ejecutivo de Gestion y Operaciones', 0, 1, 'L')
        
        self.set_draw_color(0, 210, 255)
        self.set_line_width(1)
        self.line(10, 28, 200, 28)
        self.ln(10)

    def footer(self):
        self.set_y(-18)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.5)
        self.line(10, 280, 200, 280)
        
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(100, 10, 'Sistema Web desarrollado por Adrian Villegas - 2026', 0, 0, 'L')
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'R')

class PDFService:
    @staticmethod
    def generar_reporte_general(filepath):
        pdf = PDFReporte()
        pdf.add_page()
        
        conn = obtener_conexion()
        cursor = conn.cursor(dictionary=True)

        pdf.set_font('Arial', 'B', 14)
        pdf.set_fill_color(0, 210, 255)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, '  1. Directorio de Clientes y Casos', 0, 1, 'L', True)
        pdf.ln(5)

        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()

        for u in usuarios:
            pdf.set_fill_color(245, 245, 245)
            pdf.set_font('Arial', 'B', 11)
            pdf.set_text_color(30, 30, 30)
            rol_badge = "[ADMIN]" if u['rol'] == 'admin' else "[CLIENTE]"
            pdf.cell(0, 8, f"  {rol_badge} {u['nombre']} (CI: {u['cedula']})", 1, 1, 'L', True)
            
            pdf.set_font('Arial', '', 9)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(0, 6, f"   Tel: {u['telefono']}  |  Email: {u['mail']}", 0, 1, 'L')
            pdf.cell(0, 6, f"   Dir: {u['direccion']}", 0, 1, 'L')
            
            cursor.execute("SELECT * FROM tickets WHERE id_usuario = %s", (u['id_usuario'],))
            tks = cursor.fetchall()
            
            if tks:
                pdf.set_text_color(0, 150, 200)
                for t in tks:
                    estado = t['estado'].upper()
                    pdf.cell(10, 5, "", 0, 0)
                    pdf.cell(0, 5, f"> Ticket #{t['id_ticket']}: {t['equipo']}  [{estado}]", 0, 1, 'L')
            else:
                pdf.set_text_color(180, 180, 180)
                pdf.cell(10, 5, "", 0, 0)
                pdf.cell(0, 5, "Sin actividad de soporte reciente.", 0, 1, 'L')
                
            pdf.ln(4)

        pdf.add_page()
        
        pdf.set_font('Arial', 'B', 14)
        pdf.set_fill_color(0, 210, 255)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, '  2. Resumen de Inventario (Repuestos)', 0, 1, 'L', True)
        pdf.ln(5)

        cursor.execute("SELECT * FROM productos")
        productos = cursor.fetchall()

        pdf.set_font('Arial', 'B', 10)
        pdf.set_fill_color(40, 40, 40)
        pdf.set_text_color(255, 255, 255)
        pdf.set_draw_color(40, 40, 40)
        
        pdf.cell(15, 10, ' ID', 1, 0, 'C', True)
        pdf.cell(115, 10, ' Producto / Componente', 1, 0, 'L', True)
        pdf.cell(25, 10, ' Stock', 1, 0, 'C', True)
        pdf.cell(35, 10, ' Precio ($)', 1, 1, 'R', True)

        pdf.set_font('Arial', '', 9)
        pdf.set_text_color(30, 30, 30)
        
        fill = False
        
        for p in productos:
            if fill:
                pdf.set_fill_color(240, 240, 240)
            else:
                pdf.set_fill_color(255, 255, 255)
                
            pdf.cell(15, 8, str(p['id']), 'LR', 0, 'C', fill)
            pdf.cell(115, 8, f" {p['nombre'][:60]}", 'LR', 0, 'L', fill)
            
            if p['cantidad'] <= 5:
                pdf.set_text_color(200, 0, 0)
                pdf.set_font('Arial', 'B', 9)
            else:
                pdf.set_text_color(30, 30, 30)
                pdf.set_font('Arial', '', 9)
                
            pdf.cell(25, 8, str(p['cantidad']), 'LR', 0, 'C', fill)
            
            pdf.set_text_color(30, 30, 30)
            pdf.set_font('Arial', '', 9)
            pdf.cell(35, 8, f"{p['precio']:.2f} ", 'LR', 1, 'R', fill)
            
            fill = not fill

        pdf.cell(190, 0, '', 'T', 1)

        cursor.close()
        conn.close()
        pdf.output(filepath)