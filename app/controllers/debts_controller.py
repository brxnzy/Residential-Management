from config.database import connection_db

class Debts:
    def __init__(self):
        self.db = connection_db()
        self.db.autocommit = True

    
    def get_debs(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM debts")
            debts = cursor.fetchall()
            cursor.close()
            return debts
        except Exception as e:
            print(e)
            return False
        
    
    def get_users_debts(self, user_id):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM debts WHERE id_usuario = %s", (user_id,))
            debts = cursor.fetchall()
            cursor.close()
            print(debts)
            return debts
        except Exception as e:
            print(e)
            return False
        
    def get_debtors(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
            SELECT 
                    u.id AS user_id,
                    CONCAT(u.name, ' ', u.last_name) AS resident,
                    d.amount AS debt_amount,
                    d.period,
                    d.month,
                    d.id,
                    COALESCE(
                        CONCAT( a.building, ', Apto. ', a.apartment_number),
                        CONCAT('Casa ', h.house_number)
                    ) AS residence
                FROM debts d
                JOIN users u ON u.id = d.id_usuario
                LEFT JOIN apartments a ON a.id_usuario = d.id_usuario
                LEFT JOIN houses h ON h.id_usuario = d.id_usuario
                WHERE d.amount > 0;
                """)
            debtors = cursor.fetchall()
            cursor.close()
            return debtors
        except Exception as e:
            print(e)
            return False    