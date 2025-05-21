from datetime import datetime, timedelta
from config.database import connection_db
import os
from apscheduler.schedulers.background import BackgroundScheduler
    
class Claims:
    def __init__(self, app):
        self.db = connection_db()
        self.db.autocommit = True
        self.app = app
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.update_claims_status, 'interval', minutes=1)
        self.scheduler.start()


    def update_claims_status(self):
        try:
            cursor = self.db.cursor(dictionary=True)

            # Consultar solo reclamos en estado 'atendido'
            cursor.execute("SELECT id, scheduled_date, start_time, status FROM claims WHERE status = 'atendido'")
            claims = cursor.fetchall()

            # Obtener la fecha y hora actual
            current_datetime = datetime.now()

            for claim in claims:
                scheduled_date_str = claim['scheduled_date']
                start_time = claim['start_time']

                # Verificar si algún valor es None
                if not scheduled_date_str or not start_time:
                    print(f"Reclamo {claim['id']} tiene valores nulos en fecha u horas. Se omite.")
                    continue  # Saltar este reclamo

                # Convertir `timedelta` a `time` si es necesario
                if isinstance(start_time, timedelta):
                    start_time = (datetime.min + start_time).time()

                # Formatear las horas correctamente
                start_time_str = start_time.strftime("%H:%M:%S")

                # Combinar fecha con hora para crear un datetime completo
                start_datetime = datetime.strptime(f"{scheduled_date_str} {start_time_str}", '%Y-%m-%d %H:%M:%S')

                # Cambiar de 'atendido' a 'en progreso' si current_datetime >= start_datetime
                if claim['status'] == 'atendido' and current_datetime >= start_datetime:
                    cursor.execute("UPDATE claims SET status = 'en progreso' WHERE id = %s", (claim['id'],))

            self.db.commit()  # Guardar los cambios en la base de datos
            # print("Estados de los reclamos actualizados correctamente.")
            return True

        except Exception as e:
            print(f"Error al actualizar los estados de los reclamos: {e}")
            return False



    

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

            # Guardar solo los archivos válidos (máximo 3)
            for index, file in enumerate(files[:3]):  # Máximo 3 archivos
                if file and file.filename:  # Asegúrate de que el archivo tenga nombre y contenido
                    filename = f"{claim_id}_file{index + 1}{os.path.splitext(file.filename)[1]}"
                    file_path = os.path.join(claim_folder, filename)
                    file.save(file_path)
                    evidence_files.append(filename)
                else:
                    evidence_files.append(None)  # Si no hay archivo, ponemos None

            # Columnas donde se guardarán los nombres de los archivos
            evidence_columns = ['evidence_1', 'evidence_2', 'evidence_3']

            # Actualizar solo las columnas con nombres de archivo válidos
            for i, file_name in enumerate(evidence_files):
                if file_name:  # Solo actualizamos si hay un nombre de archivo
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


    def attend_claim(self, claim_id, schedule_date, start_time, reply):
            try:
                print(f"Intentando atender el reclamo con ID: {claim_id}")
                print("la respues del admin es:", reply)
                
                cursor = self.db.cursor(dictionary=True)
                
                # Obtener el reclamo con el id proporcionado
                print("Ejecutando consulta para obtener el reclamo...")
                cursor.execute("SELECT id_usuario FROM claims WHERE id = %s AND status = 'pendiente'", (claim_id,))
                claim = cursor.fetchone()
                
                # Verificar si el reclamo fue encontrado
                if not claim:
                    print(f"Reclamo {claim_id} no encontrado o ya atendido.")
                    return False
                
                print(f"Reclamo encontrado: {claim}")
                user_id = claim['id_usuario']
                
                # Actualizar el reclamo con la nueva información
                print("Actualizando el reclamo con la nueva fecha, horario")
                cursor.execute("""
                    UPDATE claims 
                    SET scheduled_date = %s, start_time = %s, status = 'atendido'
                    WHERE id = %s
                """, (schedule_date, start_time,  claim_id))
                
                # Insertar una notificación para el usuario
                print("Insertando notificación para el usuario...")
                cursor.execute("""SELECT category, description FROM claims WHERE id = %s""", (claim_id,))
                claim = cursor.fetchone()
            
                if claim:
                    category = claim['category']
                    description = claim['description']
                    print(f'descripcion del reclamo: {description}')

                    message = f"Tu reclamo de Categoría: {category} - '{description}' / ha sido programado para {schedule_date} e inicia a las {start_time}."
                else:
                    # Si no se encuentra el reclamo, usar un mensaje genérico
                    message = f"Tu reclamo {claim_id} ha sido programado para {schedule_date} e inicia a las {start_time} ."
                
                # Insertar la notificación con el mensaje
                cursor.execute("""
                    INSERT INTO notifications (id_usuario, message, created_at, reply)
                    VALUES (%s, %s, NOW(), %s)
                """, (user_id, message, reply))
                    
                # Confirmar los cambios
                print("Confirmando los cambios en la base de datos...")
            
                
                print("Reclamo atendido y notificación enviada con éxito.")
                return True
            except Exception as e:
                print(f"Error al atender el reclamo: {e}")
                return False




    def reject_claim(self, claim_id, reject_reason):
        try:
            cursor = self.db.cursor(dictionary=True)

            # Obtener category, description y id_usuario del reclamo
            cursor.execute("""
                SELECT id_usuario, category, description 
                FROM claims 
                WHERE id = %s
            """, (claim_id,))
            claim_data = cursor.fetchone()

            # Verificar si se encontró el reclamo
            if not claim_data:
                print(f"No se encontró el reclamo con ID {claim_id}")
                cursor.close()
                return False

            user_id = claim_data['id_usuario']
            category = claim_data['category']
            description = claim_data['description']

            # Actualizar el estado del reclamo a 'rechazado'
            cursor.execute("""
                UPDATE claims 
                SET status = 'rechazado' 
                WHERE id = %s
            """, (claim_id,))
            print('Reclamo rechazado')

            # Crear el mensaje de notificación con category y description
            notification_message = f"Tu reclamo (Categoría: {category} - {description}) ha sido rechazado. Motivo: {reject_reason}"
            print(f"user_id: {user_id}, notification_message: {notification_message}")


            # Insertar la notificación
            notification_query = """
                INSERT INTO notifications (id_usuario, message, status)
                VALUES (%s, %s, 'unread')
            """
            cursor.execute(notification_query, (user_id, notification_message))

            cursor.close()

            return True
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return False



    def finish_claim(self, claim_id):
        try:
            cursor = self.db.cursor(dictionary=True)

            cursor.execute(
                "SELECT id, category, description, id_usuario FROM claims WHERE id = %s",
                (claim_id,)
            )
            claim = cursor.fetchone()

            if not claim:
                print(f"No se encontró el reclamo con ID {claim_id}")
                return False

            current_datetime = datetime.now()
            finished_at = current_datetime.date()  # Fecha de finalización
            end_time = current_datetime.time()     #

            # Actualizar el reclamo
            cursor.execute(
                "UPDATE claims SET status = 'resuelto', finished_at = %s, end_time = %s WHERE id = %s",
                (finished_at, end_time, claim_id)
            )

            # Crear el mensaje de notificación
            notification_message = (
                f" (Tu reclamo de Categoría: {claim['category']} - {claim['description']}) "
                f"terminó el día {finished_at} a la hora {end_time.strftime('%H:%M:%S')}"
            )
            user_id = claim['id_usuario']  # El ID del usuario asociado al reclamo

            # Insertar la notificación en la tabla notifications
            cursor.execute(
                "INSERT INTO notifications (id_usuario, message, created_at) VALUES (%s, %s, %s)",
                (user_id, notification_message, current_datetime)
            )

            self.db.commit()  # Guardar los cambios en la base de datos
            print('Reclamo finalizado!')
            print(f"user_id: {user_id}, notification_message: {notification_message}")

            return True

        except Exception as e:
            print('Error finalizando el reclamo:', e)
            return False


    def rate_claim(self, claim_id, rating):
        try:
            cursor = self.db.cursor(dictionary=True)

            # Actualizar la calificación y el comentario en la tabla claims
            cursor.execute("""
                UPDATE claims 
                SET rating = %s
                WHERE id = %s
            """, (rating, claim_id))

            self.db.commit()  # Guardar los cambios en la base de datos

            return True

        except Exception as e:
            print('Error al calificar el reclamo:', e)
            return False
        
    def get_claims_rating(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            query = """
                SELECT 
                    ROUND(AVG(rating), 1) AS promedio, 
                    COUNT(rating) AS cantidad 
                FROM claims 
                WHERE rating IS NOT NULL
            """
            cursor.execute(query)
            row = cursor.fetchone()

            promedio = row["promedio"] if row["promedio"] is not None else 0.0
            cantidad = row["cantidad"] if row["cantidad"] else 0

            cursor.close()

            return {
                "promedio": float(promedio),
                "cantidad": int(cantidad)
            }

        except Exception as e:
            print("An exception occurred:", e)
            return {"promedio": 0.0, "cantidad": 0}



    def get_rating_distribution(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("""
                SELECT rating, COUNT(*) as total 
                FROM claims 
                WHERE rating IS NOT NULL 
                GROUP BY rating
            """)
            rows = cursor.fetchall()
            cursor.close()

            # Inicializar arreglo [1★, 2★, 3★, 4★, 5★]
            distribution = [0, 0, 0, 0, 0]

            for row in rows:
                rating = int(row[0])
                if 1 <= rating <= 5:
                    distribution[rating - 1] = row[1]

            return distribution

        except Exception as e:
            print("An exception occurred:", e)
            return [0, 0, 0, 0, 0]


    def get_claims_category(self):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
               select * from claims_category
            """)
            categories = cursor.fetchall()
            cursor.close()

            return categories

        except Exception as e:
            print("error obteniendo las categorias de los reclamos:", e)
            return False
        
    def add_claim_category(self, category):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                INSERT INTO claims_category (name) VALUES (%s)
            """, (category,))
            self.db.commit()
            cursor.close()
            return True
        except Exception as e:
            print("error al agregar la categoria:", e)
            return False
        
    def delete_claim_category(self, category_id):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                DELETE FROM claims_category WHERE id = %s
            """, (category_id,))
            self.db.commit()
            cursor.close()
            return True
        except Exception as e:
            print("error al eliminar la categoria:", e)
            return False
        

    def update_claim_category(self,category_id, new_category):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                UPDATE claims_category SET name = %s WHERE id = %s
            """, (new_category,category_id,))
            self.db.commit()
            cursor.close()
            return True
        except Exception as e:
            print("error al actualizar la categoria:", e)
            return False