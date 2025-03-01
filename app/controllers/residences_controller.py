from config.database import connection_db
"""
Clase Apartements, donde estara toda la logica que maneja esa entidad, como por ejemplo, que esten disponibles, asignarlos, etc.
"""
class Residences:
    def __init__(self):
        self.db = connection_db()
        self.db.autocommit = True



def get_apartments(self):
    try:
        cursor = self.db.cursor(dictionary=True)
        query = """
            SELECT a.*, 
                   u.first_name AS resident_first_name, 
                   u.last_name AS resident_last_name 
            FROM apartments a
            LEFT JOIN users u ON a.id_usuario = u.id
        """
        cursor.execute(query)
        apartments = cursor.fetchall()
        cursor.close()

        for apt in apartments:
            if apt["resident_first_name"] and apt["resident_last_name"]:
                apt["resident"] = f"{apt['resident_first_name']} {apt['resident_last_name']}"
            else:
                apt["resident"] = "Sin residente"

        return apartments

    except Exception as e:
        print(f"Error obteniendo apartamentos: {e}")
        return []




    def get_houses(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM houses")
            houses = cursor.fetchall()
            cursor.close()
            return houses

        except Exception as e:
            print(f"Error obteniendo casas disponibles: {e}")
            return []  # Retorna una lista vacía si hay error