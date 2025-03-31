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


