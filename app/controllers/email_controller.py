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
        asunto = "Bienvenido a Habitat Max - Establece tu contraseña"
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







