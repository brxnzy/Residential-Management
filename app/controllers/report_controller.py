from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
import os
from config.database import connection_db

class Reports:
    def __init__(self, app):
        self.db = connection_db()
        self.db.autocommit = True
        self.app = app
        
    
    def generate_payment_report(self, id):
        try:
            cursor = self.db.cursor()
            print(f"Generando reporte de pago con ID: {id}")
            cursor.execute("SELECT id, id_usuario, amount, created_at, payment_method, paid_period FROM payments WHERE id = %s", (id,))
            payment = cursor.fetchone()
            cursor.close()

            if not payment:
                print("No se encontró el pago.")
                return
            
            # Definir ruta de guardado
            report_folder = os.path.join(self.app.config['UPLOAD_FOLDER'], "reports")
            os.makedirs(report_folder, exist_ok=True)  # Crear carpeta si no existe
            file_path = os.path.join(report_folder, f"payment_{id}.pdf")

            # Configurar PDF
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            # Estilos personalizados
            title_style = ParagraphStyle(name="TitleStyle", fontSize=18, spaceAfter=10, alignment=1, textColor=colors.darkblue)
            subtitle_style = ParagraphStyle(name="SubtitleStyle", fontSize=12, spaceAfter=8, textColor=colors.black, alignment=1)

            # Agregar Logo (Opcional)
            logo_path = os.path.join("..", "static", "img" ,"logo.png")  # Ruta del logo en uploads/static/logo.png
            if os.path.exists(logo_path):
                logo = Image(logo_path, width=50, height=50)
                elements.append(logo)

            # Encabezado
            elements.append(Paragraph("Reporte de Pago", title_style))
            elements.append(Paragraph("Habitat Max - Sistema de Gestión Residencial", subtitle_style))
            elements.append(Spacer(1, 12))

            # Datos del Pago
            table_data = [
                ["ID del Pago", payment[0]],
                ["ID del Usuario", payment[1]],
                ["Monto", f"${payment[2]:,.2f}"],
                ["Fecha", str(payment[3])],
                ["Estado", payment[4]],
            ]

            table = Table(table_data, colWidths=[120, 200])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]))

            elements.append(table)
            elements.append(Spacer(1, 20))

            # Firma
            elements.append(Paragraph("__________________________", styles["Normal"]))
            elements.append(Paragraph("Administrador", styles["Normal"]))

            # Guardar PDF
            doc.build(elements)
            print(f"Reporte guardado en: {file_path}")
            return file_path

        except Exception as e:
            print(f"Error al generar reporte de pagos: {e}")





