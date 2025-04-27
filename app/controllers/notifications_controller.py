from config.database import connection_db

class Notifications:
    def __init__(self):
        self.db = connection_db()
        self.db.autocommit = True

    
    def user_notifications(self, user_id):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute('SELECT * FROM notifications WHERE id_usuario = %s ORDER BY created_at DESC', (user_id,))
            notifications = cursor.fetchall()
            cursor.close()
            return notifications
        
        except Exception as e:
            print('Error obteniendo las notificaciones:', e)
            return []

    def mark_as_read(self, notification_id):
        try:
          cursor = self.db.cursor(dictionary=True)
          cursor.execute('UPDATE notifications SET status = "read" WHERE id = %s', (notification_id,))
          return True
        except Exception as e:
          print('Error leyendo la notificacion:', e)
          return False


    def send_payment_reminder(self, debt_id):
        try:
            cursor = self.db.cursor(dictionary=True)
            cursor.execute('Select period, month, id_usuario from debts where id = %s', (debt_id,))
            months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
            debt = cursor.fetchone()
            if debt:
                cursor.execute(
                    'INSERT INTO notifications (id_usuario, message) VALUES (%s, %s)',
                    (debt['id_usuario'], f"Recordatorio de pago: {months[debt['month']-1 ]} {debt['period']}, Porfavor realice el pago de su deuda")
                )
                return True
            else:
                print('No se encontró la deuda con el ID proporcionado.')
                return False
        
        except Exception as e:
            print('Error obteniendo las notificaciones:', e)
            return False
        
        finally:
            cursor.close()
            