from config.database import connection_db
from controllers.report_controller import Reports
from werkzeug.utils import secure_filename
import os

class Payments:
    def __init__(self, app):
        self.db = connection_db()
        self.db.autocommit = True
        self.app = app
        self.report = Reports(self.app)

        

    def get_payments(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT 
                    payments.*,
                    CONCAT(users.name, ' ', users.last_name) AS resident
                FROM payments
                INNER JOIN users ON payments.id_usuario = users.id
                order by created_at ASC
            """
            cursor.execute(query)
            payments = cursor.fetchall()
            cursor.close()
            return payments
        except Exception as e:
            print(f"Error al obtener pagos: {e}")
            return False
            
    def user_payments(self, user_id):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM payments WHERE user_id = %s", (user_id,))
            payments = cursor.fetchall()
            cursor.close()
            return payments
        except Exception as e:
            print(e)
            return False
            
    def cash_payment(self, user_id, amount, notes, debts: list):
        try:
            cursor = self.db.cursor()
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
                file_path = self.report.generate_payment_report(payment_id)  # Generar el reporte y obtener la ruta

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


    def send_transfer_request(self,user_id, evidence, description):
        try:
            cursor = self.db.cursor()
            cursor.execute("insert into transfer_requests(id_usuario,description) values(%s,%s)", (user_id, description))
            id = cursor.lastrowid

            filename = secure_filename(evidence.filename)
            extension = os.path.splitext(filename)[1]

            new_filename = f"{id}{extension}"
            upload_folder = self.app.config['UPLOAD_FOLDER']

            transfer_requests_folder = os.path.join(upload_folder, 'transfer_requests')
            if not os.path.exists(transfer_requests_folder):
                os.makedirs(transfer_requests_folder)

            file_path = os.path.join(transfer_requests_folder, new_filename)
        
          
            evidence.save(file_path)

            
            cursor.execute(
                "UPDATE transfer_requests SET evidence = %s WHERE id = %s",
                (new_filename, id)
            )

            cursor.close()

            return True

        except Exception as e:
          self.db.rollback()
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
                    COALESCE(
                        h.house_number,
                        CONCAT(a.building,' ','Apartamento ', a.apartment_number)
                    ) AS residence
                FROM transfer_requests tr
                JOIN users u ON tr.id_usuario = u.id
                LEFT JOIN houses h ON tr.id_usuario = h.id_usuario
                LEFT JOIN apartments a ON tr.id_usuario = a.id_usuario;
            """)


            transfer_requests = cursor.fetchall()
            cursor.close()
            return transfer_requests
        except Exception as e:
            print(f"Error al obtener transferencias: {e}")
            return False
