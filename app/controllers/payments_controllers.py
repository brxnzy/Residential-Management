from config.database import connection_db
from controllers.report_controller import Reports
from controllers.email_controller import EmailSender
from werkzeug.utils import secure_filename
import os

class Payments:
    def __init__(self, app):
        self.db = connection_db()
        self.db.autocommit = True
        self.app = app
        self.report = Reports(self.app)
        self.email = EmailSender()

        

    def get_payments(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT 
                    payments.*,
                    CONCAT(users.name, ' ', users.last_name) AS resident
                FROM payments
                INNER JOIN users ON payments.id_usuario = users.id
                order by created_at DESC
            """
            cursor.execute(query)
            payments = cursor.fetchall()
            cursor.close()
            return payments
        except Exception as e:
            print(f"Error al obtener pagos: {e}")
            return False
            
    def get_user_payments(self, user_id):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM payments WHERE id_usuario = %s", (user_id,))
            payments = cursor.fetchall()
            cursor.close()
            return payments
        except Exception as e:
            print(e)
            return False
            
    def cash_payment(self, user_id, amount, notes, debts: list, admin_id):
        try:
            cursor = self.db.cursor(dictionary=True)
            print("Registrando pago en efectivo")
            print(f"Parámetros recibidos - user_id: {user_id}, amount: {amount}, notes: {notes}, debts: {debts}")

            debt_ids = tuple(debts)
            print(f"debt_ids convertido a tupla: {debt_ids}")

            if not debt_ids:
                print("debt_ids está vacío, no se ejecutará la consulta SELECT")
                periods = []
            else:
                print(f"Ejecutando SELECT con debt_ids: {debt_ids}")
                cursor.execute("SELECT id, period, month FROM debts WHERE id IN (%s)" % ','.join(['%s'] * len(debt_ids)), debt_ids)
                debt_records = cursor.fetchall()
                print(f"Resultados de la consulta: {debt_records}")

                periods = []
                for debt in debt_records:
                    _, year, month = debt
                    period = f"{year}-{str(month).zfill(2)}"
                    periods.append(period)
                    print(f"Período extraído: {period}")

            if periods:
                year = periods[0][:4]
                months = [p[5:] for p in periods]
                paid_period = f"{year}, " + ", ".join(months)
            else:
                paid_period = ""

            print("Insertando pago en la tabla payments")
            cursor.execute("""
                INSERT INTO payments (id_usuario, amount, payment_method, notes, paid_period) 
                VALUES (%s, %s, 'Efectivo', %s, %s)
            """, (user_id, amount, notes, paid_period))

            payment_id = cursor.lastrowid
            print(f"ID del pago insertado: {payment_id}")

            file_path = None  # Inicializar variable para la ruta del reporte
            if payment_id:
                file_path = self.report.generate_payment_report(payment_id, admin_id)
                
                if file_path:
                    cursor.execute('SELECT email FROM users WHERE id = %s', (user_id,))
                    user = cursor.fetchone()
                    if user:
                        email = user["email"]
                        print(f"Enviando correo a {email} con archivo {file_path}")
                        self.email.send_payment_evidence(email, "¡Tu transferencia ha sido aceptada!", file_path)

                      # Generar el reporte y obtener la ruta

            if debt_ids:
                print(f"Eliminando deudas con IDs: {debt_ids}")
                cursor.execute("DELETE FROM debts WHERE id IN (%s)" % ','.join(['%s'] * len(debt_ids)), debt_ids)
            else:
                print("No hay deudas para eliminar")

            print("Cambios confirmados en la base de datos")



            cursor.execute('insert into transactions (amount, type) values (%s, "ingreso")', (amount,))
            print("Transacción de ingreso registrada")
            cursor.close()



            return payment_id, file_path  # Retornar también la ruta del reporte

        except Exception as e:
            print("Error registrando pago en efectivo:", e)
            self.db.rollback()
            cursor.close()
            return False, None  # Asegurar que retorna ambos valores


    def send_transfer_request(self, user_id, evidence, description, debt_ids):
        try:
            cursor = self.db.cursor()
            
            # Insertamos la solicitud de transferencia
            cursor.execute("INSERT INTO transfer_requests (id_usuario, description) VALUES (%s, %s)", (user_id, description))
            transfer_request_id = cursor.lastrowid  # ID de la solicitud de transferencia

            # Guardamos la evidencia
            filename = secure_filename(evidence.filename)
            extension = os.path.splitext(filename)[1]

            new_filename = f"{transfer_request_id}{extension}"
            upload_folder = self.app.config['UPLOAD_FOLDER']
            transfer_requests_folder = os.path.join(upload_folder, 'transfer_requests')

            # Crear carpeta si no existe
            if not os.path.exists(transfer_requests_folder):
                os.makedirs(transfer_requests_folder)

            file_path = os.path.join(transfer_requests_folder, new_filename)
            evidence.save(file_path)

            # Actualizamos la ruta del archivo de evidencia
            cursor.execute("UPDATE transfer_requests SET evidence = %s WHERE id = %s", (new_filename, transfer_request_id))

            # Insertamos las deudas seleccionadas en la tabla de relaciones
            for debt_id in debt_ids:
                cursor.execute("INSERT INTO transfer_requests_debts (transfer_request_id, debt_id) VALUES (%s, %s)", (transfer_request_id, debt_id))

            # Confirmamos los cambios en la base de datos
            self.db.commit()

            cursor.close()
            return True

        except Exception as e:
            self.db.rollback()  # Revertimos los cambios en caso de error
            print(f"Error al enviar la transferencia: {e}")
            return False

        
    def get_my_transfer_requests(self, user_id):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM transfer_requests WHERE id_usuario = %s", (user_id,))
            transfer_requests = cursor.fetchall()
            cursor.close()
            return transfer_requests
        except Exception as e:
            print(f"Error al obtener transferencias: {e}")
            return False
        
    def get_all_transfer_requests(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    tr.*, 
                    CONCAT(u.name, ' ', u.last_name) AS resident,
                    u.id as resident_id,
                    COALESCE(
                        h.house_number,
                        CONCAT(a.building, ' Apartamento ', a.apartment_number)
                    ) AS residence
                FROM transfer_requests tr
                JOIN users u ON tr.id_usuario = u.id
                LEFT JOIN houses h ON tr.id_usuario = h.id_usuario
                LEFT JOIN apartments a ON tr.id_usuario = a.id_usuario
                ORDER BY tr.created_at DESC;
            """)

            transfer_requests = cursor.fetchall()

            # Ahora agregamos las deudas asociadas a cada solicitud
            for tr in transfer_requests:
                cursor.execute("""
                    SELECT d.*
                    FROM transfer_requests_debts trd
                    JOIN debts d ON d.id = trd.debt_id
                    WHERE trd.transfer_request_id = %s
                """, (tr['id'],))
                tr['debts'] = cursor.fetchall()

            cursor.close()
            return transfer_requests

        except Exception as e:
            print(f"Error al obtener transferencias: {e}")
            return False



    def approve_transfer_request(self, transfer_request_id, debts: list, admin_id):
        try:
            cursor = self.db.cursor(dictionary=True)
            total_amount = 0
            periods = []

            # Buscar el usuario relacionado a la transferencia
            cursor.execute("SELECT id_usuario FROM transfer_requests WHERE id = %s", (transfer_request_id,))
            result = cursor.fetchone()
            if not result:
                print("Transferencia no encontrada.")
                return False
            user_id = result['id_usuario']

            for debt_id in debts:
                cursor.execute("SELECT amount, period, month FROM debts WHERE id = %s", (debt_id,))
                debt = cursor.fetchone()

                if debt:
                    total_amount += debt["amount"]
                    period = f"{debt['period']}-{str(debt['month']).zfill(2)}"
                    periods.append(period)

                    cursor.execute("DELETE FROM debts WHERE id = %s", (debt_id,))

            if total_amount > 0 and periods:
                year = periods[0][:4]
                months = [p[5:] for p in periods]
                paid_period = f"{year}, " + ", ".join(months)

                # Insertar pago
                cursor.execute("""
                    INSERT INTO payments (id_usuario, amount, transfer_request_id, payment_method, paid_period)
                    VALUES (%s, %s, %s, 'Transferencia', %s)
                """, (user_id, total_amount, transfer_request_id, paid_period))

                payment_id = cursor.lastrowid

                # Generar y enviar reporte
                file_path = self.report.generate_payment_report(payment_id, admin_id)
                if file_path:
                    cursor.execute('SELECT email FROM users WHERE id = %s', (user_id,))
                    user = cursor.fetchone()
                    if user:
                        email = user["email"]
                        print(f"Enviando correo a {email} con archivo {file_path}")
                        self.email.send_payment_evidence(email, "¡Tu transferencia ha sido aceptada!", file_path)

                # Registrar en transacciones y actualizar estado
                cursor.execute('INSERT INTO transactions (amount, type) VALUES (%s, "ingreso")', (total_amount,))
                cursor.execute("UPDATE transfer_requests SET status = 'approved' WHERE id = %s", (transfer_request_id,))
                cursor.execute('INSERT INTO notifications (id_usuario, message) VALUES (%s, %s)', (user_id, "Tu transferencia ha sido aprobada!"))

                self.db.commit()
            cursor.close()
            return True

        except Exception as e:
            self.db.rollback()
            print(f"Error al aprobar la transferencia: {e}")
            return False


        

    def reject_transfer_request(self, id, reason, id_usuario):
        try:
            cursor = self.db.cursor()
            cursor.execute("UPDATE transfer_requests SET status = 'rejected' WHERE id = %s", (id,))
            cursor.execute("insert into notifications (id_usuario, message) values (%s, %s)", (id_usuario, reason))
            cursor.close()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Error al rechazar la transferencia: {e}")
            return False
        

