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
                    u.id AS resident_id,
                    u.name AS resident_first_name, 
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
                    apt["resident"] = None

            return apartments

        except Exception as e:
            print(f"Error obteniendo apartamentos: {e}")
            return []


    def get_houses(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT h.*, 
                    u.id AS resident_id,
                    u.name AS resident_first_name, 
                    u.last_name AS resident_last_name 
                FROM houses h
                LEFT JOIN users u ON h.id_usuario = u.id
            """
            cursor.execute(query)
            houses = cursor.fetchall()
            cursor.close()

            for house in houses:
                if house["resident_first_name"] and house["resident_last_name"]:
                    house["resident"] = f"{house['resident_first_name']} {house['resident_last_name']}"
                else:
                    house["resident"] = None  

            return houses

        except Exception as e:
            print(f"Error obteniendo casas: {e}")
            return []


    def vacate_residence(self, property_type, property_id, resident_id):
        """ Desocupa una casa o apartamento y deshabilita al usuario en una sola transacción """
        try:
            cursor = self.db.cursor(dictionary=True)

            # Verificar datos recibidos
            print(f"🔹 Desocupando residencia: ID={property_id}, Tipo={property_type}, Id Residente={resident_id}")

            # Unificar las consultas dentro de una transacción
            query_user = "UPDATE users SET status = 'disabled' WHERE id = %s"
            query_residence = f"UPDATE {property_type} SET id_usuario = NULL, occupied = 0 WHERE id = %s"

            cursor.execute(query_user, (resident_id,))
            print("✅ Usuario deshabilitado.")

            cursor.execute(query_residence, (property_id,))
            print("✅ Residencia desocupada.")

            self.db.commit()
            print("🔹 Cambios guardados en la base de datos.")

            # 🔹 Forzar la actualización de los datos
            cursor.execute("FLUSH TABLES users")  # Refrescar la tabla
            cursor.execute("SELECT id FROM users WHERE status = 'disabled' AND id = %s", (resident_id,))
            result = cursor.fetchone()
            
            print(f"🔍 Verificación final: {result}")

            if not result:
                print("⚠️ Advertencia: El usuario no aparece como deshabilitado después de la actualización.")

            cursor.close()

        except Exception as e:
            print(f"❌ Error desocupando residencia y deshabilitando usuario: {e}")
            self.db.rollback()



