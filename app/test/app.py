import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_payment_report():
    try:
        # Datos de ejemplo
        payment = (12345, 6789, 150.75, "2025-03-22 14:30:00", "Tarjeta de Crédito")
        resident_name = "Juan Pérez"
        apartment = "A-305"
        months = "Mayo, Junio 2025"
        amount = 3000

        # Definir ruta de guardado
        report_folder = "reports"
        os.makedirs(report_folder, exist_ok=True)  # Crear carpeta si no existe
        file_path = os.path.join(report_folder, f"payment_{payment[0]}.pdf")

        # Configurar PDF
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        # Estilos personalizados
        title_style = ParagraphStyle(
            name="TitleStyle",
            fontSize=20,
            spaceAfter=10,
            alignment=1,
            textColor=colors.HexColor('#2C3E50'),
            fontName="Helvetica-Bold"
        )
        subtitle_style = ParagraphStyle(
            name="SubtitleStyle",
            fontSize=14,
            spaceAfter=8,
            alignment=1,
            textColor=colors.HexColor('#34495E'),
            fontName="Helvetica-Bold"
        )
        body_style = ParagraphStyle(
            name="BodyStyle",
            fontSize=10,
            spaceAfter=5,
            textColor=colors.black,
            leading=14,
            fontName="Helvetica"
        )
        table_header_style = ParagraphStyle(
            name="TableHeaderStyle",
            fontSize=10,
            textColor=colors.white,
            fontName="Helvetica-Bold"
        )
        signature_style = ParagraphStyle(
            name="SignatureStyle",
            fontSize=10,
            spaceBefore=20,
            alignment=1,
            textColor=colors.black,
            fontName="Helvetica"
        )

        # Ruta del logo
        logo_path = "../static/img/logo.png"
        
        # Verificar si el logo existe
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=1.5*inch, height=1.5*inch)
            logo.hAlign = "CENTER"
            elements.append(logo)
        else:
            print(f"Advertencia: Logo no encontrado en {logo_path}")

        # Encabezado
        elements.append(Spacer(1, 10))
        elements.append(Paragraph("Pinares del Norte", title_style))
        elements.append(Paragraph("RECIBO DE PAGO", subtitle_style))
        elements.append(Spacer(1, 20))

        # Datos del recibo
        receipt_data = [
            [Paragraph("Fecha de Pago:", table_header_style), payment[3]],
            [Paragraph("Método de Pago:", table_header_style), payment[4]],
            [Paragraph("ID del Pago:", table_header_style), payment[0]],
            [Paragraph("ID del Usuario:", table_header_style), payment[1]],
        ]
        table_receipt = Table(receipt_data, colWidths=[150, 250])
        table_receipt.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor('#2980B9')),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elements.append(table_receipt)
        elements.append(Spacer(1, 15))

        # Datos del pago
        payment_data = [
            [Paragraph("Residente:", table_header_style), resident_name],
            [Paragraph("Apartamento:", table_header_style), apartment],
            [Paragraph("Meses Pagados:", table_header_style), months],
            [Paragraph("Monto Total:", table_header_style), f"${amount:,.2f}"]
        ]
        table_payment = Table(payment_data, colWidths=[150, 250])
        table_payment.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor('#2980B9')),
            ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey)
        ]))
        elements.append(table_payment)
        elements.append(Spacer(1, 20))

        # Mensaje de agradecimiento
        elements.append(Paragraph("Gracias por su puntualidad en el pago. Su compromiso ayuda al mantenimiento del residencial.", body_style))
        elements.append(Spacer(1, 30))

        # Firma
        elements.append(Paragraph("__________________________", signature_style))
        elements.append(Paragraph("Administrador de Pinares del Norte", signature_style))

        # Guardar PDF
        doc.build(elements)
        print(f"Reporte guardado en: {file_path}")

    except Exception as e:
        print(f"Error al generar el reporte de pago: {e}")

# Ejecutar la función
generate_payment_report()