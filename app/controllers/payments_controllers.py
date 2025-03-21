from config.database import connection_db
from controllers.report_controller import Reports

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
                # Usar %s como marcador de posición y pasar debt_ids como parámetro
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
            print(f"Período pagado formateado: {paid_period}")

            print("Insertando pago en la tabla payments")
            cursor.execute("""
                INSERT INTO payments (id_usuario, amount, payment_method, notes, paid_period) 
                VALUES (%s, %s, 'Efectivo', %s, %s)
            """, (user_id, amount, notes, paid_period))

            payment_id = cursor.lastrowid
            print(f"ID del pago insertado: {payment_id}")
            if payment_id:
                self.report.generate_payment_report(payment_id)


            if debt_ids:
                print(f"Eliminando deudas con IDs: {debt_ids}")
                cursor.execute("DELETE FROM debts WHERE id IN (%s)" % ','.join(['%s'] * len(debt_ids)), debt_ids)
            else:
                print("No hay deudas para eliminar")


            print("Cambios confirmados en la base de datos")
            cursor.close()
            return True
        except Exception as e:
            print("Error registrando pago en efectivo:", e)
            self.db.rollback()
            cursor.close()
            return False
