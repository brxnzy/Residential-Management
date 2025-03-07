from config.database import connection_db
import os
"""
Clase Claims, donde estara toda la logica que maneja esa entidad, como por ejemplo, crear un reclamo, etc.
"""
class Claims:
    def __init__(self, app):
        self.db = connection_db()
        self.db.autocommit = True
        self.app = app

    

    def send_claim(self, user_id, category, description, files):
        try:
            # Obtener nombre y apellido del usuario desde la base de datos
            cursor = self.db.cursor(dictionary=True)
            query = "SELECT name, last_name FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()
            
            if not user:
                print("Usuario no encontrado")
                return False
            
            name_lastname = f"{user['name'].strip()}_{user['last_name'].strip()}"


            # Insertar el reclamo en la base de datos
            query = """
                INSERT INTO claims (id_usuario, category, description)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (user_id, category, description))
            self.db.commit()

            claim_id = cursor.lastrowid  # Obtener el ID del reclamo insertado

            # Construir la carpeta para almacenar evidencias
            upload_folder = self.app.config['UPLOAD_FOLDER']
            claim_folder = os.path.join(upload_folder, 'evidences', name_lastname)

            # Crear la carpeta si no existe
            os.makedirs(claim_folder, exist_ok=True)

            # Lista para guardar los nombres de los archivos
            evidence_files = []

            # Guardar los archivos en la carpeta
            for index, file in enumerate(files[:3]):  # Máximo 3 archivos
                filename = f"{claim_id}_file{index + 1}{os.path.splitext(file.filename)[1]}"
                file_path = os.path.join(claim_folder, filename)
                file.save(file_path)
                evidence_files.append(filename)

            # Columnas donde se guardarán los nombres de los archivos
            evidence_columns = ['evidence_1', 'evidence_2', 'evidence_3']

            # Bucle para actualizar solo las columnas necesarias
            for i, file_name in enumerate(evidence_files):
                update_query = f"""
                UPDATE claims
                SET {evidence_columns[i]} = %s
                WHERE id = %s
                """
                cursor.execute(update_query, (file_name, claim_id))

            self.db.commit()

            return True

        except Exception as e:
            print(f"Error al enviar reclamo: {e}")
            return False

            

    def get_my_claims(self, user_id):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM claims WHERE id_usuario = %s ORDER BY created_at DESC", (user_id,))
            claims = cursor.fetchall()
            return claims
        except Exception as e:
            print('Un error ocurrió:', e)
            return []
        finally:
            cursor.close()  


    def get_all_claims(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
            SELECT c.*, u.name AS name, u.last_name AS last_name,
                    COALESCE(
                        CONCAT('Building ', a.building, ', Apt ', a.apartment_number),
                        CONCAT('House ', h.house_number)
                    ) AS residence
                FROM claims c
                JOIN users u ON c.id_usuario = u.id
                LEFT JOIN apartments a ON c.id_usuario = a.id_usuario
                LEFT JOIN houses h ON c.id_usuario = h.id_usuario
                ORDER BY c.created_at DESC
            """)
            claims = cursor.fetchall()
            return claims
        except Exception as e:
            print('Un error ocurrió:', e)
            return []
        finally:
            cursor.close()

