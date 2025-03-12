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