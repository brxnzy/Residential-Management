from config.database import connection_db
"""
Clase Apartements, donde estara toda la logica que maneja esa entidad, como por ejemplo, que esten disponibles, asignarlos, etc.
"""
class Apartments:
    def __init__(self):
        self.db = connection_db()
        self.db.autocommit = True



    def get_apartments(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM apartments")
            apartments = cursor.fetchall()
            cursor.close()
            return apartments

        except Exception as e:
            print(f"Error obteniendo apartamentos disponibles: {e}")
            return []  # Retorna una lista vacía si hay error
