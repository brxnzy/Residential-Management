import yagmail
from flask import flash
from email_validator import validate_email, EmailNotValidError
import os
from dotenv import load_dotenv


class EmailSender:
    def __init__(self):
        path_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
        load_dotenv(path_env)

        self.email_user = os.getenv("EMAILUSER")
        self.email_password = os.getenv("EMAILPASSW")

        # Iniciar conexión con yagmail
        self.yag = yagmail.SMTP(self.email_user, self.email_password)

    def validar_correo(self, correo):
        """Valida si un correo es válido."""
        try:
            valid = validate_email(correo)
            return valid.email
        except EmailNotValidError as e:
            print(f"Correo inválido: {e}")
            return None

    def enviar_correo(self, destinatario, name, last_name, cedula, user_id):
        """Envía un correo en formato HTML con enlace de establecimiento de contraseña."""
        asunto = "Bienvenido a Pinares del Norte - Establece tu contraseña"
        enlace = f"http://127.0.0.1:5000/activate_account/{user_id}"

        contenido = f"""
            <html>
            <body>
                <h1 style="color: blue;">¡Bienvenido, {name} {last_name}!</h1>
                <p>Tu cédula registrada es <b>{cedula}</b>.</p>
                <p>Para completar tu registro, haz clic en el botón de abajo y establece tu contraseña.</p>
                <a href='{enlace}' style="display: inline-block; padding: 10px 20px; color: white; background-color: blue; text-decoration: none; border-radius: 5px;">
                    Establecer Contraseña
                </a>
                <br>
                <p>Si no solicitaste este acceso, ignora este mensaje.</p>
            </body>
            </html>
        """
        try:
            self.yag.send(to=destinatario, subject=asunto, contents=contenido)
            print("Correo enviado exitosamente a:", destinatario)
        except Exception as e:
            print(f"Error al enviar el correo: {e}")

    def custom_email(self, destinatario, asunto, mensaje):
        """Envía un correo con un asunto y mensaje personalizado en formato HTML."""
        contenido = f"""
            <html>
            <body>
                <h1>{mensaje}</h1>
            </body>
            </html>
        """
        try:
            self.yag.send(to=destinatario, subject=asunto, contents=contenido)
            print("Correo enviado exitosamente a:", destinatario)
        except Exception as e:
            print(f"Error al enviar el correo: {e}")

    def send_payment_evidence(self, destinatario, mensaje, ruta_archivo):
            """Envía un correo con un archivo adjunto como evidencia de pago."""
            asunto = "Evidencia de Pago - Habitat Max"
            print("Ruta del archivo:", ruta_archivo)
            print('DESTINATARIO:', destinatario)
            contenido_html = f"""
                <html>
                <body>
                    <p>{mensaje}</p>
                    <p>Se adjunta evidencia de pago para su validación.</p>
                </body>
                </html>
            """
            try:
                # Verificar si el archivo existe
                if not os.path.isfile(ruta_archivo):
                    raise FileNotFoundError(f"El archivo {ruta_archivo} no existe o no es accesible.")

                # Enviar el correo con el archivo adjunto
                self.yag.send(
                    to=destinatario,
                    subject=asunto,
                    contents=contenido_html,
                    attachments=ruta_archivo
                )
                print("Correo con evidencia enviado exitosamente a:", destinatario)
            except Exception as e:
                print(f"Error al enviar el correo con evidencia: {e}")

    # Prueba del método





