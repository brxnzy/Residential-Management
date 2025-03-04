from config.database import connection_db
from werkzeug.utils import secure_filename
from controllers.email_controller import EmailSender
from flask import flash
import os
"""
Clase Resident, donde estara toda la logica que maneja esa entidad, como por ejemplo, enviar reclamos, pagos, etc.
"""
class Resident:
    def __init__(self,app):
        self.db = connection_db()
        self.email = EmailSender()
        self.db.autocommit = True
        self.app = app

    
    
    def update_photo(self, user_id, photo):
        if photo:
            try:
                filename = secure_filename(photo.filename)
                extension = os.path.splitext(filename)[1].lower()
                
                allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".svg"}
                if extension not in allowed_extensions:
                    print("Formato de imagen no permitido.")
                    return False
                
                new_filename = f"{user_id}{extension}"
                file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], new_filename)

                # Eliminar archivos antiguos con el mismo user_id pero diferente extensión
                for ext in allowed_extensions:
                    old_file = os.path.join(self.app.config['UPLOAD_FOLDER'], f"{user_id}{ext}")
                    if os.path.exists(old_file) and old_file != file_path:
                        os.remove(old_file)

                # Guardar la nueva foto
                photo.save(file_path)

            
                cursor = self.db.cursor()
                cursor.execute("UPDATE users SET photo = %s WHERE id = %s", (new_filename, user_id))

                self.db.commit()
                cursor.close()

                print("Foto actualizada:", new_filename)
                return True
            
            except Exception as e:
                print(f"Error al actualizar la foto: {e}")
                return False
        return False


    def delete_photo(self,user_id):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute('UPDATE users SET photo = NULL WHERE id = %s', (user_id,))
            print('Foto eliminada correctamente')
            return True
        
        except Exception as e:
            flash('Error eliminando la foto', 'error')
            print('Error eliminando la foto')
            return False


    def update_info(self, user_id, email, phone):
        try:
            valid_email = self.email.validar_correo(email)
            if not valid_email:
                print("El correo proporcionado no es válido.")
                flash("El correo proporcionado no es válido.", "error")
                return False

            query = "UPDATE users SET email = %s, phone = %s WHERE id = %s"
            cursor = self.db.cursor(dictionary=True)
            cursor.execute(query, (valid_email, phone, user_id))
            self.db.commit()
            cursor.close()
            self.email.custom_email(valid_email, "Actualización de información",
                            "Has actualizado correctamente tu información. Gracias por preferirnos.")

            print("Información actualizada y correo de confirmación enviado.")
            return True

        except Exception as e:
            print(f"Error al actualizar la información: {e}")
            return False



