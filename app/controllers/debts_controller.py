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
        
    