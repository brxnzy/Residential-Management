import os
from config.database import connection_db
from werkzeug.utils import secure_filename 

class Settings:
    def __init__(self):
        self.db = connection_db()
        self.db.autocommit = True

    def update_logo(self, file):
        try:
            if file:
                base_dir = os.path.dirname(os.path.abspath(__file__))
                logo_path = os.path.join(base_dir, "..", "static", "img", "logo.png")
                
                file.save(logo_path)
                return True  
        except Exception as e:
            print(f"Error al actualizar el logo: {e}")
            return False  # Fallo

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