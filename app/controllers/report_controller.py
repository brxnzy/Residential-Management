from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Line
import os
from datetime import datetime
from config.database import connection_db

class Reports:
    def __init__(self, app):
        self.db = connection_db()
        self.db.autocommit = True
        self.app = app
        

    def generate_payment_report(self, id, admin_id):
        try:
            cursor = self.db.cursor(dictionary=True)
            print(f"Generando factura con ID: {id} y Admin ID: {admin_id}")
            
            # Consulta para obtener los datos del pago
            query_payment = """
                SELECT 
                    p.id, 
                    p.id_usuario, 
                    p.amount, 
                    p.created_at, 
                    p.payment_method, 
                    p.paid_period,
                    u.name AS user_name, 
                    u.last_name AS user_last_name,
                    u.email,
                    u.Phone,
                    a.apartment_number,
                    h.house_number
                FROM payments p
                JOIN users u ON p.id_usuario = u.id
                LEFT JOIN apartments a ON p.id_usuario = a.id_usuario
                LEFT JOIN houses h ON p.id_usuario = h.id_usuario
                WHERE p.id = %s
            """
            cursor.execute(query_payment, (id,))
            payment_info = cursor.fetchone()

            if not payment_info:
                print("No se encontró el pago.")
                cursor.close()
                return

            # Consulta para obtener el nombre del administrador
            query_admin = """
                SELECT name, last_name 
                FROM users 
                WHERE id = %s
            """
            cursor.execute(query_admin, (admin_id,))
            admin_info = cursor.fetchone()
            cursor.close()

            # Verificar si se encontró el administrador
            if not admin_info:
                print(f"No se encontró el administrador con ID: {admin_id}")
                admin_full_name = "Desconocido"
            else:
                admin_full_name = f"{admin_info['name']} {admin_info['last_name']}"

            # Extract data del pago
            payment_id = payment_info["id"]
            user_id = payment_info["id_usuario"]
            amount = payment_info["amount"]
            created_at = payment_info["created_at"]
            payment_method = payment_info["payment_method"]
            paid_period = payment_info["paid_period"]
            user_name = payment_info["user_name"]
            user_last_name = payment_info["user_last_name"]
            user_email = payment_info['email']
            user_phone = payment_info['Phone']
            apartment_number = payment_info["apartment_number"]
            house_number = payment_info["house_number"]

            resident_name = f"{user_name} {user_last_name}"
            housing = apartment_number if apartment_number else (house_number if house_number else "N/A")
            months = paid_period if paid_period else "N/A"

            # Define save path                        
            # Definir ruta de guardado
            report_folder = os.path.join(self.app.config['UPLOAD_FOLDER'], "reports")
            os.makedirs(report_folder, exist_ok=True)  # Crear carpeta si no existe
            file_path = os.path.join(report_folder, f"payment_{id}.pdf")
            # Custom colors
            primary_color = colors.HexColor('#A6A6A6')  
            secondary_color = colors.HexColor('#adadad')
            gray = colors.HexColor('#242424')  # Gris claro para fondos
            green = colors.HexColor('#157f3d')
            green2 = colors.Color(21/255, 127/255, 61/255, alpha=0.3)
            
            # Configure PDF
            doc = SimpleDocTemplate(
                file_path, 
                pagesize=letter,
                topMargin=0.5*inch,  
                bottomMargin=0.7*inch,
                leftMargin=0.7*inch,
                rightMargin=0.7*inch
            )

            elements = []
            styles = getSampleStyleSheet()

            # Custom styles for better appearance
            title_style = ParagraphStyle(
                name="TitleStyle",
                fontSize=18,
                spaceAfter=2,
                alignment=0,  # 0 = Left align
                textColor=colors.black,
                fontName="Helvetica-Bold"
            )
            
            subtitle_style = ParagraphStyle(
                name="SubtitleStyle",
                fontSize=16,
                spaceAfter=15,
                alignment=0,
                textColor=colors.black,
                fontName="Helvetica-Bold"
            )
            
            header_style = ParagraphStyle(
                name="HeaderStyle",
                fontSize=10,
                textColor=colors.black,
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
            
            company_info_style = ParagraphStyle(
                name="CompanyInfoStyle",
                fontSize=9,
                textColor=gray,
                fontName="Helvetica",
                alignment=0,
                leading=12
            )
            
            client_info_style = ParagraphStyle(
                name="ClientInfoStyle",
                fontSize=9,
                textColor=colors.black,
                fontName="Helvetica",
                alignment=0,
                leading=14
            )
            
            total_style = ParagraphStyle(
                name="TotalStyle",
                fontSize=12,
                textColor=colors.black,
                fontName="Helvetica-Bold",
                alignment=2  # Right align
            )

            # Create header table with logo and company info
            try:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                logo_path = os.path.join(base_dir, "..", "static", "img", "logo.png")
                logo_path = os.path.normpath(logo_path)
                if os.path.exists(logo_path):
                    logo_img = Image(logo_path, width=1.4*inch, height=1.4*inch)
                    has_logo = True
                else:
                    print("Logo not found. Using text header.")
                    has_logo = False
            except Exception as e:
                print(f"Error loading logo: {e}")
                has_logo = False

            # Create header with two columns: logo and invoice title
            if has_logo:
                header_data = [
                    [logo_img, Paragraph('<br/><br/><br/><b>Residencial Pinares del Norte</b><br/><br/>Factura de Mantenimiento', title_style)]
                ]
            else:
                header_data = [
                    [Paragraph('<b>Residencial XYZ</b>', title_style), 
                    Paragraph('<b>Factura de Pago de Mantenimiento</b>', subtitle_style)]
                ]

            header_table = Table(header_data, colWidths=[2*inch, 4*inch])
            header_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ]))
            elements.append(header_table)
            
            # Add a horizontal line
            d = Drawing(500, 1)
            d.add(Line(0, 0, 500, 0, strokeColor=colors.black, strokeWidth=1))
            elements.append(d)
            elements.append(Spacer(1, 15))
            
            # Two column layout for company and client info
            company_info = Paragraph("""
                <b>Dirección:</b> Santo Domingo D.N., Gualey  <br/>
                <b>Teléfono:</b> 849-284-2781<br/>
                <b>Email:</b> respinaresdelnorte@gmail.com<br/>
            """, company_info_style)
            
            # Current date from payment info
            payment_date = created_at.strftime("%d-%m-%Y")
            
            invoice_info = Paragraph(f"""
                <b>Fecha del pago:</b> {payment_date}<br/>
                <b>ID de Pago:</b> {payment_id}<br/>
                <b>Atendido por:</b> {admin_full_name}
            """, company_info_style)
            
            info_data = [[company_info, invoice_info]]
            info_table = Table(info_data, colWidths=[3.2*inch, 3.2*inch])
            info_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ALIGN', (0, 0), (0, 0), 'LEFT'),
                ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ]))
            elements.append(info_table)
            elements.append(Spacer(1, 15))
            
            # Client information section with background
            client_header = Paragraph("<b>INFORMACIÓN DEL RESIDENTE</b>", header_style)
            elements.append(client_header)
            
            # Line under client header
            d = Drawing(500, 1)
            d.add(Line(0, 0, 500, 0, strokeColor=secondary_color, strokeWidth=1))
            elements.append(d)
            elements.append(Spacer(1, 5))
            
            client_info = Paragraph(f"""
                <b>Residente:</b> {resident_name}<br/>
                <b>Residencia:</b> {housing}<br/>
                <b>Teléfono:</b> {user_phone if user_phone else 'N/A'}<br/>
                <b>Email:</b> {user_email if user_email else 'N/A'}<br/>
            """, client_info_style)
            elements.append(client_info)
            elements.append(Spacer(1, 15))
            
            # Payment details section
            payment_header = Paragraph("<b>DETALLE DE PAGOS</b>", header_style)
            elements.append(payment_header)
            
            # Line under payment header
            d = Drawing(500, 1)
            d.add(Line(0, 0, 500, 0, strokeColor=secondary_color, strokeWidth=1))
            elements.append(d)
            elements.append(Spacer(1, 10))
            
            # Payment details table with improved styling
            data = [
                ["Período", "Descripción", "Monto", "Método de Pago"],
                [months, "Cuota de Mantenimiento", f"${amount:,.2f}", payment_method],
            ]
            
            table = Table(data, colWidths=[1.2*inch, 2.2*inch, 1.5*inch, 1.5*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), green),  # Header background
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header text color
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 7),
                ('TOPPADDING', (0, 0), (-1, 0), 7),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Body background
                ('GRID', (0, 0), (-1, -1), 0.5, colors.white),  # Thinner grid lines
                ('LINEABOVE', (0, 0), (-1, 0), 1, colors.white),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.white),
                ('LINEBELOW', (0, -1), (-1, -1), 1, colors.white),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, green2])  # Alternating row colors
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 15))
            
            # Summary and total table
            summary_data = [
                ["", ""],
                ["Subtotal:", f"${amount:,.2f}"],
                ["ITBIS (0%):", "$0.00"],
                ["Total:", f"${amount:,.2f}"]
            ]
            
            summary_table = Table(summary_data, colWidths=[5*inch, 1.4*inch])
            summary_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('FONTNAME', (0, 1), (0, -2), 'Helvetica'),
                ('FONTNAME', (0, -1), (1, -1), 'Helvetica-Bold'),
                ('LINEABOVE', (0, -1), (1, -1), 1, colors.white),
                ('LINEBELOW', (0, -1), (1, -1), 1, colors.white),
                ('BACKGROUND', (0, -1), (1, -1), green2),
            ]))
            elements.append(summary_table)
            elements.append(Spacer(1, 20))
            
            # Footer section
            footer_text = Paragraph("""
                <font size="10" color="#666666">
                <b>Nota:</b> Este pago corresponde al mantenimiento mensual del condominio. Por favor conserve este comprobante para futuros reclamos.<br/>
                Para cualquier consulta, contacte a la administración: respinaresdelnorte@gmail.com | Tel: (849) 284-2781
                </font>
            """, styles['Normal'])
            elements.append(footer_text)
            
            # Build the PDF
            doc.build(elements)
            print(f"Factura generada exitosamente en: {file_path}")
            return file_path

        except Exception as e:
            print(f"Error al generar la factura: {e}")
            return None

