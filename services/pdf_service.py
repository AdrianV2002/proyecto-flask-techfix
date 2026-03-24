from fpdf import FPDF
from services.producto_service import ProductoService

class PDFReporte(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.set_text_color(13, 110, 253)
        self.cell(0, 10, 'Reporte de Inventario - Sistema Web', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

class PDFService:
    @staticmethod
    def generar_reporte_productos(filepath):
        productos = ProductoService.obtener_todos()
        pdf = PDFReporte()
        pdf.add_page()
        
        pdf.set_font('Arial', 'B', 12)
        pdf.set_fill_color(33, 37, 41)
        pdf.set_text_color(255, 255, 255)
        
        pdf.cell(20, 10, 'ID', 1, 0, 'C', True)
        pdf.cell(90, 10, 'Producto', 1, 0, 'C', True)
        pdf.cell(30, 10, 'Stock', 1, 0, 'C', True)
        pdf.cell(40, 10, 'Precio ($)', 1, 1, 'C', True)
        
        pdf.set_font('Arial', '', 11)
        pdf.set_text_color(0, 0, 0)
        
        for p in productos:
            pdf.cell(20, 10, str(p['id']), 1, 0, 'C')
            pdf.cell(90, 10, p['nombre'][:40], 1, 0, 'L')
            pdf.cell(30, 10, str(p['cantidad']), 1, 0, 'C')
            pdf.cell(40, 10, f"{p['precio']:.2f}", 1, 1, 'C')
            
        pdf.output(filepath)