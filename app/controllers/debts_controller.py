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
        
    