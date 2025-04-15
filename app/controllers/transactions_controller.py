from config.database import connection_db


class Transactions:
    def __init__(self):
        self.db = connection_db()
        self.db.autocommit = True

    
    def get_balance(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT 
                    (SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'ingreso') -
                    (SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'gasto') 
                    AS total_balance;
            """)

            balance = cursor.fetchone()
            return balance['total_balance']
        
        except Exception as e:
            print(f"Error al obtener balance: {e}")
            return None
    
    def get_monthly_incomes(self):
        try:
            cursor = self.db.cursor()
            query = """
                SELECT MONTH(created_at) as month, SUM(amount) as total
                FROM transactions
                WHERE type = 'ingreso'
                GROUP BY MONTH(created_at)
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            monthly_totals = [0] * 12
            for row in results:
                month_index = row[0] - 1  # Enero = 0
                monthly_totals[month_index] = float(row[1])
            
            return monthly_totals
        except Exception as e:
            print(f"Error al obtener ingresos mensuales: {e}")
            return [0] * 12

        
    def get_monthly_expenses(self):
        try:
            cursor = self.db.cursor()
            query = """
                SELECT MONTH(created_at) as month, SUM(amount) as total
                FROM transactions
                WHERE type = 'gasto'
                GROUP BY MONTH(created_at)
            """
            cursor.execute(query)
            results = cursor.fetchall()
            
            monthly_totals = [0] * 12
            for row in results:
                month_index = row[0] - 1
                monthly_totals[month_index] = float(row[1])
            
            return monthly_totals
        except Exception as e:
            print(f"Error al obtener gastos mensuales: {e}")
            return [0] * 12


    def get_community_status(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT 
                    (SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'ingreso') AS total_incomes,
                    (SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE type = 'gasto') AS total_expenses
            """
            cursor.execute(query)
            result = cursor.fetchone()

            total_incomes = result['total_incomes']
            total_expenses = result['total_expenses']

            if total_incomes == 0:
                percentage = 0
            else:
                difference = total_incomes - total_expenses
                percentage = round((difference / total_incomes) * 100, 2)

            return {
                "incomes": total_incomes,
                "expenses": total_expenses,
                "percentage": percentage
            }

        except Exception as e:
            print(f"Error al obtener estado financiero de la comunidad: {e}")
            return {
                "incomes": 0,
                "expenses": 0,
                "percentage": 0
            }


    def get_payment_method_stats(self):
        try:
            cursor = self.db.cursor()
            query = """
                SELECT payment_method, COUNT(*) as total
                FROM payments
                GROUP BY payment_method
            """
            cursor.execute(query)
            results = cursor.fetchall()

            total_payments = sum([row[1] for row in results])

            method_stats = []
            for row in results:
                method = row[0]
                count = row[1]
                percentage = round((count / total_payments) * 100, 2)
                method_stats.append({
                    "label": f"{method} ({count} pagos - {percentage}%)",
                    "value": count
                })

            return method_stats
        except Exception as e:
            print(f"Error al obtener métodos de pago: {e}")
            return []

    def get_all_expenses(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT t.*, CONCAT(u.name, ' ', u.last_name) AS admin
                FROM transactions t
                JOIN users u ON t.admin_id = u.id
                WHERE t.type = 'gasto'
                order by t.created_at DESC
            """
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Error al obtener gastos: {e}")
            return False
        
    def register_expense(self,amount,reason,admin_id):
        try:
            cursor = self.db.cursor()
            query = """
                INSERT INTO transactions (amount, reason, type, admin_id)
                VALUES (%s, %s, 'gasto', %s)
            """
            cursor.execute(query, (amount, reason, admin_id))
            return True
        except Exception as e:
            print(f"Error al registrar gasto: {e}")
            return False