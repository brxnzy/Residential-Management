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
        <body style="background-color: #f4f4f4; padding: 20px; font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: auto; background-color: white; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 30px;">
                <h2 style="color: #2c3e50; text-align: center;">¡Bienvenido a Pinares del Norte!</h2>
                <p style="font-size: 16px; color: #333;">Hola <b>{name} {last_name}</b>,</p>
                <p style="font-size: 15px; color: #555;">Hemos registrado tu cédula: <b>{cedula}</b>.</p>
                <p style="font-size: 15px; color: #555;">Para completar tu registro y comenzar a usar nuestra plataforma, por favor haz clic en el siguiente botón para establecer tu contraseña:</p>
                <div style="text-align: center; margin: 20px 0;">
                    <a href="{enlace}" style="background-color: #007bff; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-size: 16px;">
                        Establecer Contraseña
                    </a>
                </div>
                <p style="font-size: 14px; color: #999;">Si no solicitaste este acceso, puedes ignorar este mensaje.</p>
                <hr style="margin-top: 30px;">
                <p style="text-align: center; font-size: 12px; color: #ccc;">Pinares del Norte &copy; 2025</p>
            </div>
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





