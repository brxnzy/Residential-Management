from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
import os

# Definir carpeta de almacenamiento
UPLOAD_FOLDER = "uploads/reports"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
file_path = os.path.join(UPLOAD_FOLDER, "test_payment_report.pdf")

# Configurar PDF
doc = SimpleDocTemplate(file_path, pagesize=letter)
elements = []
styles = getSampleStyleSheet()

# Estilos personalizados
title_style = ParagraphStyle(name="TitleStyle", fontSize=18, spaceAfter=10, alignment=1, textColor=colors.darkblue)
subtitle_style = ParagraphStyle(name="SubtitleStyle", fontSize=12, spaceAfter=8, textColor=colors.black, alignment=1)

# Agregar Título
elements.append(Paragraph("Reporte de Pago (Prueba)", title_style))
elements.append(Paragraph("Habitat Max - Sistema de Gestión Residencial", subtitle_style))
elements.append(Spacer(1, 12))

# Datos Falsos del Pago
table_data = [
    ["ID del Pago", "9999"],
    ["ID del Usuario", "5555"],
    ["Monto", "$1,250.00"],
    ["Fecha", "2025-03-20"],
    ["Estado", "Completado"],
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

# Generar PDF
doc.build(elements)
print(f"Reporte de prueba generado: {file_path}")
