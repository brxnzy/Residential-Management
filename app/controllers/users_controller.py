from flask import session, flash, redirect, url_for
from config.database import connection_db
from auth.login import Auth
from controllers.email_controller import EmailSender
from werkzeug.utils import secure_filename
import requests
import os


class Users:
    def __init__(self,app):
        self.app =  app
        self.db = connection_db()
        self.db.autocommit = True
        self.auth = Auth()
        self.smtp = EmailSender()


    def get_residents(self):
        try:
            cursor = self.db.cursor(dictionary=True) 
            # Consulta para obtener todos los usuarios con el rol "resident"
            cursor.execute("""
                SELECT u.*
                FROM users u
                JOIN user_roles ur ON u.id = ur.user_id
                JOIN roles r ON ur.role_id = r.id
                WHERE r.name = 'resident' AND u.status != 'disabled'
            """)
            residents = cursor.fetchall()  # Obtiene todos los resultados
            return residents

        except Exception as e:
            print(f"Error al obtener residentes: {e}")
            return []

    def get_admins(self):
        try:
            cursor = self.db.cursor(dictionary=True)

            # Consulta para obtener todos los usuarios con el rol "resident"
            cursor.execute("""
                SELECT u.*
                FROM users u
                JOIN user_roles ur ON u.id = ur.user_id
                JOIN roles r ON ur.role_id = r.id
                 WHERE r.name = 'admin' AND u.status != 'disabled'
            """)
            admins= cursor.fetchall()  # Obtiene todos los resultados
            return admins

        except Exception as e:
            print(f"Error al obtener residentes: {e}")
            return []


    def get_disabled_users(self):
        try:
            cursor = self.db.cursor(dictionary=True)

            cursor.execute("""
                SELECT 
                    u.*, 
                    GROUP_CONCAT(r.name SEPARATOR ', ') AS roles  -- Concatena los roles en una columna
                FROM users u
                JOIN user_roles ur ON u.id = ur.user_id
                JOIN roles r ON ur.role_id = r.id
                WHERE u.status = 'disabled'
                GROUP BY u.id  -- Agrupa por usuario para evitar duplicados
            """)
            
            disabled_users = cursor.fetchall()  
            return disabled_users

        except Exception as e:
            print(f"Error al obtener usuarios deshabilitados: {e}")
            return []

    def get_user_by_id(self, user_id):
        """Obtiene toda la información del usuario, sus roles y la información del apartamento o casa (si aplica)."""
        try:
            with self.db.cursor(dictionary=True) as cursor:
                # Obtener información del usuario
                user_query = "SELECT * FROM users WHERE id = %s"
                cursor.execute(user_query, (user_id,))
                user = cursor.fetchone()

                if not user:
                    return None  # Si el usuario no existe, retorna None

                # Obtener los roles del usuario
                roles_query = """
                    SELECT r.name 
                    FROM roles r
                    INNER JOIN user_roles ur ON r.id = ur.role_id
                    WHERE ur.user_id = %s
                """
                cursor.execute(roles_query, (user_id,))
                roles = [row["name"] for row in cursor.fetchall()]  # Convertir roles a lista

                # Convertir la lista de roles en un string separado por comas
                user["role"] = ", ".join(roles) if roles else "No roles"

                # Verificar si el usuario tiene asignado un apartamento
                apartment_query = """
                    SELECT building, apartment_number 
                    FROM apartments 
                    WHERE id_usuario = %s
                """
                cursor.execute(apartment_query, (user_id,))
                apartment = cursor.fetchone()

                if apartment:
                    user["building"] = apartment["building"] 
                    user["apartment_number"] = apartment["apartment_number"]
                else:
                    # Si no tiene apartamento, buscar en la tabla de casas
                    house_query = """
                        SELECT house_number 
                        FROM houses 
                        WHERE id_usuario = %s
                    """
                    cursor.execute(house_query, (user_id,))
                    house = cursor.fetchone()

                    if house:
                        # Si el usuario tiene una casa asignada, agregar la información
                        user["house"] = house["house_number"]

                return user

        except Exception as e:
            print(f"Error al obtener usuario: {e}")
            return None






    def add_user(self, cedula, name, last_name, email, phone, is_admin, is_resident, property_type, property_id):
        try:
            if not self.smtp.validar_correo(email):
                flash("Correo electrónico inválido", "error")
                return 

            cursor = self.db.cursor(dictionary=True)

            # Insertar usuario
            cursor.execute("""
                INSERT INTO users (id_card, name, last_name, email, Phone)
                VALUES (%s, %s, %s, %s, %s)
            """, (cedula, name, last_name, email, phone))
            self.db.commit()

            cursor.execute("SELECT LAST_INSERT_ID() AS id")
            user_id = cursor.fetchone()['id']

            # Agregar roles (si es administrador o residente)
            if is_admin:
                cursor.execute("""
                    INSERT INTO user_roles (user_id, role_id)
                    VALUES (%s, 1)
                """, (user_id,))
            if is_resident:
                cursor.execute("""
                    INSERT INTO user_roles (user_id, role_id)
                    VALUES (%s, 2)
                """, (user_id,))
                print("residente agregado")

                if property_type == "apartamentos" and property_id:
                    cursor.execute("""
                        UPDATE apartments 
                        SET id_usuario = %s , occupied = 1
                        WHERE id = %s
                    """, (user_id, property_id))
                    print("apartamento asignado")
                    self.db.commit()

                elif property_type == "casas" and property_id:
                    cursor.execute("""
                        UPDATE houses 
                        SET id_usuario = %s , occupied = 1
                        WHERE id = %s
                    """, (user_id, property_id))
                    print("casa asignada")
                    self.db.commit()

            
                

            self.db.commit()
            cursor.close()

            # Enviar correo de confirmación
            self.smtp.enviar_correo(email, name, last_name, cedula, user_id)
            flash("Usuario agregado y correo enviado exitosamente", "success")

        except Exception as e:
            # Manejo de errores específicos
            if "Duplicate entry" in str(e):
                flash("El correo o cédula ya están registrados.", "error")
            elif "foreign key constraint" in str(e):
                flash("Error de base de datos: verifique las relaciones de usuario.", "danger")
            else:
                flash(f"Ocurrió un error inesperado: {e}", "danger")


            print(f"Error agregando el usuario: {e}")

            cursor.close()



    
    def update_user_roles(self, user_id, is_admin, is_resident, property_type=None, property_id=None):
        try:
            cursor = self.db.cursor(dictionary=True)

            # Obtener los roles actuales del usuario
            cursor.execute("SELECT role_id FROM user_roles WHERE user_id = %s", (user_id,))
            current_roles = {row['role_id'] for row in cursor.fetchall()}  

            # Determinar los nuevos roles según los checkboxes seleccionados
            new_roles = {1} if is_admin else set()
            new_roles.add(2) if is_resident else None

            # Roles a agregar y eliminar
            roles_to_add = new_roles - current_roles
            roles_to_remove = current_roles - new_roles

            # Agregar nuevos roles
            if roles_to_add:
                cursor.executemany(
                    "INSERT INTO user_roles (user_id, role_id) VALUES (%s, %s)",
                    [(user_id, role_id) for role_id in roles_to_add]
                )

            # Eliminar roles no deseados
            if roles_to_remove:
                cursor.executemany(
                    "DELETE FROM user_roles WHERE user_id = %s AND role_id = %s",
                    [(user_id, role_id) for role_id in roles_to_remove]
                )

                # Si se quita el rol de residente, liberar la residencia
                if 2 in roles_to_remove:
                    cursor.execute("UPDATE apartments SET id_usuario = NULL, occupied = 0 WHERE id_usuario = %s", (user_id,))
                    cursor.execute("UPDATE houses SET id_usuario = NULL, occupied = 0 WHERE id_usuario = %s", (user_id,))

            # Si se asigna el rol de residente, asignar propiedad si se proporcionó una
            if is_resident and property_type and property_id:
                if property_type == "apartamentos":
                    cursor.execute("UPDATE apartments SET id_usuario = %s, occupied = 1 WHERE id = %s", (user_id, property_id))
                elif property_type == "casas":
                    cursor.execute("UPDATE houses SET id_usuario = %s, occupied = 1 WHERE id = %s", (user_id, property_id))

            # Guardar cambios solo si hubo modificaciones
            if roles_to_add or roles_to_remove or (is_resident and property_type and property_id):
                self.db.commit()

            return True  # Éxito

        except mysql.connector.Error as e:
            print(f"Error editando los roles del usuario: {e}")
            self.db.rollback()
            return False  # Fallo

        finally:
            cursor.close()



    def assign_property(self, user_id, property_type, property_id):
        try:
            cursor = self.db.cursor(dictionary=True)

            print(f"Intentando asignar propiedad {property_id} de tipo {property_type} al usuario {user_id}")

            # Verificar si el usuario ya tiene una propiedad asignada
            cursor.execute("""
                SELECT id FROM apartments WHERE id_usuario = %s
                UNION
                SELECT id FROM houses WHERE id_usuario = %s
            """, (user_id, user_id))
            existing_property = cursor.fetchone()


            if existing_property:
                print(f"Error: El usuario {user_id} ya tiene una propiedad asignada.")
                flash("Este usuario ya tiene una propiedad asignada", "warning")
                return

            # Si la propiedad es un apartamento o una casa, actualizar la relación
            if property_type == 'apartamentos':
                cursor.execute("""
                    UPDATE apartments
                    SET occupied = 1, id_usuario = %s
                    WHERE id = %s AND occupied = 0
                """, (user_id, property_id))
                print(f"Ejecutando UPDATE para apartamento {property_id}")

            elif property_type == 'casas':
                cursor.execute("""
                    UPDATE houses
                    SET occupied = 1, id_usuario = %s
                    WHERE id = %s AND occupied = 0
                """, (user_id, property_id))
                print(f"Ejecutando UPDATE para casa {property_id}")

            # Habilitar al usuario si estaba deshabilitado
            cursor.execute("""
                UPDATE users
                SET status = 'enabled'
                WHERE id = %s
            """, (user_id,))
            print(f"Usuario {user_id} activado")

            self.db.commit()
            flash("Propiedad asignada exitosamente", "success")

        except Exception as e:  # <- El except ahora está alineado correctamente
            print(f"Error asignando propiedad: {e}")
            flash(f"Error al asignar propiedad: {e}", "danger")



 

    
    def disable_user(self, id):
        try:
            cursor = self.db.cursor(dictionary=True)

            print(f"Intentando deshabilitar al usuario {id}")

            # Verificar si el usuario tiene el rol de "resident"
            cursor.execute("""
                SELECT r.name FROM roles r
                JOIN user_roles ur ON r.id = ur.role_id
                WHERE ur.user_id = %s
            """, (id,))
            roles = [row["name"] for row in cursor.fetchall()]

            if "resident" in roles:
                print(f"Usuario {id} es residente, verificando vivienda...")

                # Buscar si el usuario tiene una vivienda asignada
                cursor.execute("""
                    SELECT id FROM apartments WHERE id_usuario = %s
                    UNION
                    SELECT id FROM houses WHERE id_usuario = %s
                """, (id, id))
                property_data = cursor.fetchone()

                if property_data:
                    property_id = property_data["id"]
                    print(f"Usuario {id} vive en la propiedad {property_id}, liberándola...")

                    # Actualizar la propiedad para dejarla libre
                    cursor.execute("""
                        UPDATE apartments SET occupied = 0, id_usuario = NULL WHERE id = %s
                    """, (property_id,))
                    
                    cursor.execute("""
                        UPDATE houses SET occupied = 0, id_usuario = NULL WHERE id = %s
                    """, (property_id,))

            # Deshabilitar al usuario
            cursor.execute("""
                UPDATE users
                SET status = 'disabled'
                WHERE id = %s
            """, (id,))

            self.db.commit()
            flash("Usuario deshabilitado exitosamente", "success")
            print(f"Usuario {id} deshabilitado correctamente")

        except Exception as e:
            print(f"Error disabling user: {e}")
            flash(f"Error al deshabilitar usuario: {e}", "danger")



    def enable_user(self,id):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("""
                UPDATE users
                SET status = 'enabled'
                WHERE id = %s
            """, (id,))
            self.db.commit()
            flash("Usuario habilitado exitosamente", "success")
        except Exception as e:
            print(f"Error disabling user: {e}")
            flash(f"Error al habilitar usuario: {e}", "danger")

    def delete_user(self, id):
        try:
            cursor = self.db.cursor(dictionary=True)
            
            # Liberar la propiedad en apartments si el usuario está asignado
            cursor.execute("SELECT id FROM apartments WHERE id_usuario = %s", (id,))
            apartment = cursor.fetchone()
            if apartment:
                cursor.execute("UPDATE apartments SET id_usuario = NULL, occupied = 0 WHERE id = %s", (apartment["id"],))
                self.db.commit()

            # Liberar la propiedad en houses si el usuario está asignado
            cursor.execute("SELECT id FROM houses WHERE id_usuario = %s", (id,))
            house = cursor.fetchone()
            if house:
                cursor.execute("UPDATE houses SET id_usuario = NULL, occupied = 0 WHERE id = %s", (house["id"],))
                self.db.commit()

            # Ahora eliminamos el usuario
            cursor.execute("DELETE FROM users WHERE id = %s", (id,))
            
            
            self.db.commit()
            cursor.close()
            flash("Usuario eliminado permanentemente!", "success")

        except Exception as e:
            self.db.rollback()  # Revierte cambios en caso de error
            print(f"Error eliminando usuario: {e}")
            flash(f"Error eliminando usuario: {e}", "danger")







    def save_user_photo(self, user_id, photo):
        if photo:
            try:
                filename = secure_filename(photo.filename)
                extension = os.path.splitext(filename)[1]
    
                # Crea un nuevo nombre único basado en el user_id
                new_filename = f"{user_id}{extension}"
                
                # Define el path donde se guardará la foto (asumiendo que 'UPLOAD_FOLDER' está en config)
                file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], new_filename)
                
                # Guarda la imagen en el directorio especificado
                photo.save(file_path)
                
                # Devuelve el nombre del archivo guardado para almacenarlo en la base de datos
                return new_filename
                print("foto:", new_filename)
            except Exception as e:
                print(f"Error al guardar la foto: {e}")
                return None
        return None




    def activate_account(self, user_id, file, password):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
            user = cursor.fetchone()

            if user:
                current_password = user.get('password')
                if not current_password:  # Si el usuario no tiene contraseña, procede con la activación
                    hashed_password = self.auth.hash_password(password)
                    photo_path = None
                    if file:
                        photo_path = self.save_user_photo(user_id, file)

                    cursor.execute("""
                        UPDATE users
                        SET password = %s, photo = %s
                        WHERE id = %s
                    """, (hashed_password, photo_path, user_id))

                    self.db.commit() 
                    cursor.close()

                    self.db.close()

                    self.db = connection_db() 
                    print('cuenta activada correctamente')
                    
                    flash("Cuenta activada correctamente.", "success")
                else:
                    flash("El usuario ya tiene una contraseña. No se puede activar nuevamente.", "error")
            else:
                flash("Usuario no encontrado.", "error")

        except Exception as e:
            flash(f"Error activando la cuenta: {e}", "error")
            self.db.rollback()  # Rollback si ocurre un error








