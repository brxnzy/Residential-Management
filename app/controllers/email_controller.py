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
        <body style="background-color: #f9fafb; padding: 20px; font-family: Arial, sans-serif;">
            <div style="max-width: 600px; margin: auto; background-color: #fefefe; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 30px;">
                <h2 style="color: black; font-size: 35px;">¡Bienvenido a Pinares del Norte!</h2>
                <p style="font-size: 24px; color: #374151;">Hola <b>{name} {last_name}</b>,</p>
                <p style="font-size: 22px; color: #6b7280;">Hemos registrado tu cédula: <b>{cedula}</b>.</p>
                <p style="font-size: 22px; color: #6b7280;">Para completar tu registro y comenzar a usar nuestra plataforma, por favor haz clic en el siguiente botón para establecer tu contraseña:</p>
<a href="{enlace}" style="background-color: #15803d; color: white; padding: 12px; text-decoration: none; border-radius: 5px; font-size: 18px; display: inline-block;">Establecer Contraseña</a>

                <p style="font-size: 16px; color: #9ca3af;">Si no solicitaste este acceso, puedes ignorar este mensaje.</p>
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
            asunto = "Evidencia de Pago - Pinares del Norte"
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

                        
    def send_reset_email(self, to_email, reset_link):
        try:
            subject = "Restablecer tu contraseña"

            body = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Restablecer Contraseña</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f9fafb; margin: 0; padding: 0; margin-top: 0;">
    <table align="center" width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; background-color: #fefefe; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
        <tr>
            <td style="padding: 20px;">
                
                <h2 style="color: black; font-size: 28px; margin-bottom: 16px;">Restablecer tu contraseña</h2>
                <p style="font-size: 20px; color: #374151; margin-bottom: 24px;">Recibimos una solicitud para restablecer tu contraseña.</p>
                <p style="font-size: 18px; color: #6b7280; margin-bottom: 24px;">Haz clic en el botón de abajo para continuar.</p>
                <div>
                    <a href="{reset_link}" style="display: inline-block; background-color: #15803d; color: white; padding: 16px; border-radius: 6px; font-size: 20px; text-decoration: none;">
                        Restablecer Contraseña
                    </a>
                </div>
                <p style="font-size: 18px; color: #9ca3af; margin-top: 24px;">Si no solicitaste este cambio, puedes ignorar este mensaje.</p>
            </td>
        </tr>
    </table>
</body>
</html>
        """

            self.yag.send(to=to_email, subject=subject, contents=body)
            return {
                "success": True,
                "message": f"Correo de restablecimiento enviado correctamente a {to_email}"
            }
        except Exception as e:
            error_message = f"Error al enviar el correo a {to_email}: {str(e)}"
            print(error_message)
            return {
                "success": False,
                "message": error_message
            }

