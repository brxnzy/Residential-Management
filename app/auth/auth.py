from flask import session, flash, redirect, url_for
from config.database import connection_db
import bcrypt
from itsdangerous import URLSafeTimedSerializer


class Auth:
    def __init__(self, app):
        self.db = connection_db()
        self.serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

    def generate_token(self, user_id):
        token = self.serializer.dumps(user_id, salt='password-reset-salt')
        return token
    
    def hash_password(self, plain_password):
        """Hashea una contraseña usando bcrypt."""
        return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, plain_password, hashed_password):
        """Verifica una contraseña contra su hash."""
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def Login(self, cedula, plain_password):
        """Autentica un usuario usando cédula y contraseña."""
        try:
            db = connection_db()  # Crear una nueva conexión a la base de datos
            cursor = db.cursor(dictionary=True)

            print(f"Buscando usuario con cédula: {cedula}") 
            cursor.execute("SELECT * FROM users WHERE id_card = %s", (cedula,))

            user = cursor.fetchone()

            if not user:
                print(f"No se encontró un usuario con cédula: {cedula}")
                flash("Usuario o contraseña incorrectos.", 'error')
                return redirect(url_for('login'))


            print(f"Usuario encontrado: {user}")
            print(f"foto del usuario: {user['photo']}")

            # Verificar si la contraseña es correcta
            if not self.check_password(plain_password, user['password']):
                print(f"Contraseña incorrecta para usuario {cedula}")
                flash("Usuario o contraseña incorrectos.", 'error')
                return redirect(url_for('login'))

            # Obtener los roles del usuario
            cursor.execute("""
                SELECT r.name 
                FROM roles r
                JOIN user_roles ur ON ur.role_id = r.id
                WHERE ur.user_id = %s
            """, (user['id'],))
            roles = cursor.fetchall()
            role_names = [role['name'] for role in roles]

            print(f"Roles del usuario: {role_names}")

            # Configurar sesión
            session['user_id'] = user['id']
            session['roles'] = role_names
            session['status'] = user['status']
            session['user'] = user

            # Si el usuario es residente, obtener su residencia
            if 'resident' in role_names:
                session['user']['residence'] = "No residence assigned"  # Inicializa para evitar KeyError
                cursor.execute("""
                    SELECT a.apartment_number, a.building, h.house_number
                    FROM users u
                    LEFT JOIN apartments a ON u.id = a.id_usuario
                    LEFT JOIN houses h ON u.id = h.id_usuario
                    WHERE u.id = %s;
                """, (user['id'],))

                result = cursor.fetchone()

                if result:
                    if result['apartment_number'] and result['building']:
                        session['user']['residence'] = f"{result['building']} - Apartamento {result['apartment_number']}"
                    elif result['house_number']:
                        session['user']['residence'] = f"Casa {result['house_number']}"

                print(f"Residencia del usuario: {session['user']['residence']}")

            cursor.close()
            db.close()

            if user['status'] == 'disabled':
                return 'disabled'

            # Redirección según el rol del usuario
            if 'admin' in role_names:
                flash("Inicio de sesión exitoso como administrador.", 'success')
                return 'admin'
            else:
                flash("Inicio de sesión exitoso como residente.", 'success')
                return 'resident'

        except Exception as e:
            print(f"Error en Login: {e}")  
            flash("Error al iniciar sesión. Intenta nuevamente.", 'error')
            return redirect(url_for('login'))

