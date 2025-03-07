from flask import Flask, render_template, redirect, url_for, request, session, flash, make_response, abort
import bcrypt
from auth.login import Auth
from controllers.users_controller import Users
from controllers.residences_controller import  Residences
from controllers.resident_controller import  Resident
from controllers.claims_controller import Claims
from functools import wraps
import os


class App:
    def __init__(self):
        self.app = Flask(
            __name__, 
            static_folder=os.path.join(os.path.dirname(__file__), 'static'), 
            static_url_path='/static'
        )
        self.principal_routes()
        self.error_handler()
        self.auth = Auth()
        self.user = Users(self.app)
        self.resident = Resident(self.app)
        self.residences = Residences()
        self.claims = Claims(self.app)
        self.app.config['SECRET_KEY'] = 'secretkey'
        UPLOAD_FOLDER = r'C:\Users\Crist\OneDrive\Documents\Desktop\Final Proyect\app\static\uploads'
        self.app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    def error_handler(self):


        @self.app.errorhandler(403)
        def forbidden_error(e):
            return render_template('errors/403.html'), 403 

        @self.app.errorhandler(404)
        def page_not_found(e):
            return render_template('errors/404.html'), 404 

    def login_required(self, f):
            """
            Middleware para proteger rutas según el prefijo de la URL.
            /admin → Requiere rol 'admin'
            /resident → Requiere rol 'resident'
            """
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if 'user_id' not in session:
                    flash('Debes iniciar sesión para acceder', 'warning')
                    return redirect(url_for('login'))

                # Obtener el usuario desde la base de datos
                user = self.user.get_user_by_id(session['user_id'])
                if not user or user['status'] == 'disabled':  # Verificar si el usuario está deshabilitado
                    flash('Tu cuenta está deshabilitada', 'danger')
                    return redirect(url_for('disabled'))  # Ruta que muestra el mensaje de usuario deshabilitado

                path = request.path  
                required_role = None  

                if path.startswith('/admin'):
                    required_role = 'admin'
                elif path.startswith('/resident'):
                    required_role = 'resident'

                if required_role and required_role not in session.get('roles', []):
                    abort(403)  

                return f(*args, **kwargs)

            return decorated_function


    def nocache(self, f):
        """
        Decorador para deshabilitar la caché de una página.
        """
        @wraps(f)
        def nocache_wrapper(*args, **kwargs):
            response = make_response(f(*args, **kwargs))
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            return response
        return nocache_wrapper

    def principal_routes(self):
        """
        Rutas principales de la app, incluidas las del dashboard.
        """
        @self.app.route('/login', methods=['GET', 'POST'])
        @self.nocache 
        def login():
            if request.method == 'POST':
                cedula = request.form['id_card']
                password = request.form['password']
                authz = self.auth.Login(cedula, password)
                status = session.get('status')
                if status == 'disabled':
                    return redirect(url_for('disabled'))

                if authz == 'admin':
                    return redirect(url_for('dashboard'))
                elif authz == 'resident':
                    return redirect(url_for('home'))
                else:
                    return redirect(url_for('login'))
                    
           
            return render_template('secure/login.html')


        @self.app.route('/disabled')
        def disabled():
            return render_template('errors/disabled.html')

        @self.app.route('/logout')
        def logout():
            message = request.args.get('flash_message')  # Recibe el mensaje desde la URL
            session.clear()
            
            if message:
                flash(message, "success")
            flash('Cerraste sesion exitosamente', 'success')
                
            
            return redirect(url_for('login'))





        """ Rutas para el Dashboard """
                
        @self.app.route('/admin', defaults={'section': 'main', 'sub_section': None})
        @self.app.route('/admin/<section>/', defaults={'sub_section': None})
        @self.app.route('/admin/<section>/<sub_section>')
        @self.login_required
        @self.nocache
        def dashboard(section, sub_section):
            sections = {
            'main': 'admin/main.html',
            'users': 'admin/users.html',
            'my_info': 'admin/my_info.html',
            'user_info': 'admin/user_info.html',
            'residences': 'admin/residences.html',
            'claims': 'admin/claims.html'
        }
 

            residents, admins, disabled, selected_user, houses, claims = {}, {}, {}, {},{},{}
            apartments = self.residences.get_apartments() 
            houses = self.residences.get_houses() 
            claims = self.claims.get_all_claims()

            

           
         
            # 📌 Si la sección es "users", obtenemos los datos de usuarios
            if section == 'users':
                residents['residents'] = self.user.get_residents()
                admins['admins'] = self.user.get_admins()
                disabled['disabled'] = self.user.get_disabled_users()

            # 📌 Si la sección es "user_info" y se pasa un user_id, obtenemos la información del usuario
            user_id = request.args.get('user_id', type=int)
            if section == 'user_info' and user_id:
                selected_user = self.user.get_user_by_id(user_id)
                print(selected_user)

            # 📌 Mapeo correcto de la plantilla según la sección y subsección
            key = f"{section}/{sub_section}" if sub_section else section
            if key not in sections:
                return render_template('errors/404.html'), 404
            template = sections[key]  

            # Obtener el usuario de la sesión
            session_user = session.get('user')

            return render_template(
                'admin/dashboard.html',
                content_template=template,
                user=session_user,
                section=section,
                sub_section=sub_section,
                **residents,
                **admins,
                **disabled,
                houses=houses,
                apartments=apartments,
                usuario=selected_user,
                claims=claims
            )


        """ Rutas de administracion """
        

        @self.app.route('/admin/add_user', methods=['POST'])
        @self.login_required
        def add_user():
            if request.method == 'POST':
                cedula = request.form['id_card']
                name = request.form['name']
                last = request.form['last_name']
                email = request.form['email']
                phone = request.form['phone']
                
                is_admin = 'is_admin' in request.form and request.form['is_admin'] == '1'
                is_resident = 'is_resident' in request.form and request.form['is_resident'] == '1'
           
                property_type = request.form.get('propertyType') if is_resident else None
                property_id = request.form.get('propertyList') if is_resident else None
                print(f"Tipo de Propiedad:{property_type}")
                print(property_id)

                try:
                    self.user.add_user(cedula, name, last, email, phone, is_admin, is_resident, property_type, property_id)
                    return redirect(url_for('dashboard', section='users'))  
                except Exception as e:
                    flash(f"Error al agregar usuario: {e}", "danger")
                    return redirect(url_for('dashboard', section='users')) 

            return redirect(url_for('dashboard', section='users'))



        @self.app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
        def delete_user(user_id):
            try:
                self.user.delete_user(user_id)
            except Exception as e:
                print(f"Error al eliminar usuario: {e}")
            return redirect(url_for('dashboard', section='users'))

                


        @self.app.route('/admin/disable_user/<int:user_id>', methods=['POST'])
        def disable_user(user_id):
            try:
                self.user.disable_user(user_id)
            except Exception as e:
                print(f"Error al deshabilitar usuario: {e}")
            return redirect(url_for('dashboard', section='users'))


        @self.app.route('/admin/enable_user/<int:user_id>', methods=['POST'])
        def enable_user(user_id):
            try:
                self.user.enable_user(user_id)
            except Exception as e:
                print(f"Error al habilitar usuario: {e}")
            return redirect(url_for('dashboard', section='users'))

        @self.app.route('/admin/update_roles/<int:user_id>', methods=['POST'])
        def update_user_roles(user_id):
            try:
                selected_roles = request.form.getlist("roles")
                property_type = request.form.get("propertyType")
                property_id = request.form.get("propertyList")

                is_admin = 'admin' in selected_roles
                is_resident = 'resident' in selected_roles


                update = self.user.update_user_roles(user_id, is_admin, is_resident, property_type, property_id)

                if update:
                    flash("Roles actualizados correctamente", "success")
                else:
                    flash("No se realizaron cambios en los roles", "info")

            except Exception as e:
                print(f"Error al editar usuario: {e}")
                flash("Hubo un problema al actualizar los roles", "error")

            return redirect(url_for('dashboard', section='users'))


        @self.app.route('/admin/assign_property/<int:user_id>', methods=['POST'])
        def assign_property(user_id):
            try:
                # Obtenemos los valores del formulario de la propiedad
                property_type = request.form.get("propertyType")
                property_id = request.form.get("propertyList")
                print(property_type)
                print(property_id)

                # Verificamos si el tipo de propiedad es válido y si se ha seleccionado una propiedad
                if property_type and property_id:
                    # Asignamos la propiedad al usuario
                    assign = self.user.assign_property(user_id, property_type, property_id)
                    if assign:
                        flash("Propiedad asignada correctamente", "success")
                else:
                    flash("Debe seleccionar un tipo de propiedad y una residencia", "warning")
                
            except Exception as e:
                print(f"Error al asignar propiedad: {e}")
                flash("Hubo un problema al asignar la propiedad", "danger")

            return redirect(url_for('dashboard', section='users'))








        @self.nocache 
        @self.app.route('/activate_account/<int:user_id>', methods=['GET', 'POST'])
        def activate_account(user_id):
            user = self.user.get_user_by_id(user_id)

            if not user:
                flash("Usuario no encontrado.", "error")
                return redirect(url_for('login'))

          
            if user.get('password'):
                flash("Tu cuenta ya está activada. Inicia sesión.", "info")
                return redirect(url_for('login'))



            if request.method == 'POST':
                passw = request.form['password']
                photo = request.files.get('photo')
                
                if not passw:
                    flash("Debes proporcionar una contraseña.", "error")
                    return render_template("activate_acc.html", user=user)

                try:
                    self.user.activate_account(user_id, photo, passw)
                    # flash("Cuenta activada exitosamente. Ahora puedes iniciar sesión.", "success")
                    return redirect(url_for('login'))
                except Exception as e:
                    flash(f"Error al habilitar usuario: {e}", "error")

            return render_template("secure/activate_acc.html", user=user)


        @self.app.route('/admin/user_info/<int:user_id>')
        def user_info(user_id):
            try:               
                user = self.user.get_user_by_id(user_id)

                if user['status'] == 'disabled':
                    flash('Usuario deshabilitado, no se encontró información', 'error')
                    return redirect(url_for('dashboard', section='users')) 
                else:
                    print(user)
                    return redirect(url_for('dashboard', section='user_info', user_id=user_id))

            except Exception as e:
                # Manejo de excepciones si algo sale mal
                print(f"Error al obtener usuario: {e}")  # Para depuración
                flash('Ocurrió un error al obtener la información del usuario', 'error')
                return redirect(url_for('dashboard', section='users'))  # Siempre redirige en caso de error

            # En caso de que ningún bloque de código se ejecute correctamente, también redirige por defecto
            return redirect(url_for('dashboard', section='users'))


        """ Rutas para el manejo de residencias """


        @self.app.route('/admin/residences/vacate_residence', methods=['POST'])
        def vacate_residence():
            try:
                resident_id = request.form.get("residentId")
                residence_id = request.form.get("residenceId")
                residence_type = request.form.get("residenceType")


                self.residences.vacate_residence(residence_type, residence_id,resident_id)
                flash("Residencia desocupada correctamente", "success")

            except Exception as e:
                print(f"Error al desocupar residencia: {e}")
                flash("Hubo un problema al desocupar la residencia", "danger")

            return redirect(url_for('dashboard', section='residences'))





        """ Rutas para el manejo del residente """
        
        @self.app.route('/resident')
        @self.login_required
        @self.nocache  
        def home():
            id = session.get('user_id')
            user = self.user.get_user_by_id(id)
            claims = self.claims.get_my_claims(id)
            return render_template('resident/home.html', user=user, claims=claims)


        @self.app.route('/resident/update_photo/<int:user_id>', methods=['POST'])
        def update_photo(user_id):
            try:
                photo = request.files.get('photo')
                
                if not photo or photo.filename == '':
                    flash('No se seleccionó ninguna foto', 'error')
                    print('[ERROR] No se seleccionó ninguna foto')
                    return redirect(request.referrer)

                if self.resident.update_photo(user_id, photo):
                    flash('Foto actualizada correctamente', 'success')
                    print(f'[INFO] Foto actualizada para el usuario {user_id}')
                else:
                    flash('Error al actualizar la foto', 'error')
                    print(f'[ERROR] No se pudo actualizar la foto para el usuario {user_id}')

                return redirect(url_for('home'))
            
            except Exception as e:
                print(f'[EXCEPTION] Error en update_photo: {e}')
                flash('Ocurrió un error inesperado', 'error')
                return redirect(request.referrer)



        @self.app.route('/resident/delete_photo/<int:user_id>', methods=['POST'])
        def delete_photo(user_id):
            try:
                if self.resident.delete_photo(user_id):
                    flash('Foto eliminada correctamente', 'success')
                    print('foto eliminada correctamente')
                return redirect(url_for('home'))  # Redirigir al usuario a su perfil después de borrar la foto.
            except Exception as e:
                print('Error', e)
                flash('Error al eliminar la foto', 'danger')
                return redirect(url_for('home'))




        @self.app.route('/resident/update_info/<int:user_id>', methods=['POST'])
        def update_info(user_id):
            try:
                if request.method == 'POST':
                    email = request.form.get('email')
                    phone = request.form.get('phone')

                    if self.resident.update_info(user_id, email, phone):
                        flash("Credenciales editadas correctamente!", "success")
                    else:
                        flash("Error al actualizar la información.", "error")

            except Exception as e:
                print(f"Error en la ruta update_info: {e}")
                flash("Ocurrió un error al procesar la solicitud.", "error")

            return redirect(url_for('home'))





        @self.app.route('/resident/update_password/<int:user_id>', methods=['POST'])
        def update_password(user_id):
            try:
                print(f"[DEBUG] Procesando actualización de contraseña para usuario ID: {user_id}")

                current_password = request.form.get('current_password')
                print(current_password)
                new_password = request.form.get('new_password')
                confirm_password = request.form.get('confirm_password')

                print("[DEBUG] Datos recibidos correctamente")

                # Intentar actualizar la contraseña
                if self.resident.update_password(user_id, current_password, new_password, confirm_password):
                    print("[DEBUG] Contraseña actualizada exitosamente")
                    flash("Contraseña actualizada correctamente", "success")
                    return redirect(url_for('logout', flash_message='Cambiaste tu contraseña'))
                else:
                    flash("Error al actualizar la contraseña. Verifica tu información.", "error")
                    print("[DEBUG] Error en la actualización de la contraseña")

                return redirect(url_for('home')) 

            except Exception as e:
                flash("Error interno del servidor", "error")
                print(f"[DEBUG] Error en update_password: {e}")
                return redirect(url_for('home')) 
 

        @self.app.route('/resident/send_claim', methods=['POST'])
        def send_claim():
            try:
                if request.method == 'POST':
                    # Obtén el id del usuario de la sesión
                    user_id = session.get('user_id')  # Debes usar user_id, no id
                    print('id del usuario', user_id)
                    
                    # Obtén los datos del formulario
                    category = request.form.get('category')
                    description = request.form.get('description')
                    evidences = request.files.getlist('evidences')
                    
                    print('Category: ', category)
                    print('Description: ', description)
                    print('Evidences: ', evidences)
                    
                    # Llamamos a la función send_claim
                    if self.claims.send_claim(user_id, category, description, evidences):
                        flash('reclamo enviado correctamente', 'success')
                        return redirect(url_for('home')) 
                    flash('Ocurrio un Error mandando tu reclamo', 'error')
                    return redirect(url_for('home'))

            except Exception as e:
                print(f'An exception occurred: {e}')
                return redirect(url_for('home')) \


            

        @self.app.route('/')
        def redirect_to_dashboard():
            return redirect(url_for('dashboard', section='main'))


    def run(self):
        self.app.run(debug=True, port=5000)

