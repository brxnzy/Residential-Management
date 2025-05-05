# 🏘️ Pinares del Norte – Residential Management System

Pinares del norte es una aplicación de gestión residencial desarrollada con **Flask**, **MySQL**, y **TailwindCSS**. Permite administrar pagos, reportes, reclamos, residentes, roles y más desde un panel intuitivo para usuarios y administradores.

---

## 🚀 Instalación

> Asegúrate de tener **Python 3.10 o superior** y **pip** correctamente instalados.

### 1. Clona el repositorio

```bash
git clone https://github.com/brxnzy/Residential-Management.git
cd Residential-Management
```

### 2. Instala las dependencias necesarias

```bash
pip install -r requirements.txt
```

## ⚙️ Base de datos MySQL

### 1. Crear base de datos

Abre tu gestor de base de datos MySQL y crea una base de datos. y asegurate de copiar el script que esta en el archivo sql que esta dentro de app que contiene todas las tablas.

```sql
CREATE DATABASE pinares_del_norte;
```

### 2. Configurar conexión en .env

Crea un archivo llamado `.env` en la raíz del proyecto con el siguiente contenido:

```env
DB_HOST=localhost
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=pinares_del_norte
```

Reemplaza `tu_usuario` y `tu_contraseña` con tus datos reales de conexión MySQL.

## 3. Configuración de la API de Gmail y Contraseña de Aplicación

Si planeas utilizar la API de Gmail o enviar correos electrónicos desde tu cuenta de Gmail, necesitarás configurar una **contraseña de aplicación** para tu cuenta de Google. Aquí están los pasos para hacerlo:

1. **Habilita la verificación en dos pasos** para tu cuenta de Google si aún no lo has hecho.
2. **Genera una contraseña de aplicación** siguiendo estos pasos:
   * Ve a tu cuenta de Google: [https://myaccount.google.com](https://myaccount.google.com).
   * En el menú de la izquierda, haz clic en  **Seguridad** .
   * Desplázate hacia abajo hasta la sección **Acceso a Google** y selecciona  **Contraseñas de aplicaciones** .
   * Selecciona el tipo de dispositivo (puede ser "Otro" si no aparece un dispositivo específico) y luego haz clic en  **Generar** .
   * Guarda la contraseña generada, ya que la necesitarás más tarde.

### Variables de entorno

con el  `.env` ya creado en la raíz del proyecto y agrega las siguientes variables de entorno:

```bash
EMAILUSER="tu_email@gmail.com"
EMAILPASSW="tu_contraseña_de_aplicación"
```

Reemplaza:

* `tu_email@gmail.com` con tu dirección de correo electrónico de Gmail.
* `tu_contraseña_de_aplicación` con la contraseña de aplicación generada en los pasos anteriores.

> **Nota** : La contraseña de aplicación no es la misma que tu contraseña normal de Gmail. Es una contraseña única que se genera específicamente para su uso en aplicaciones externas.
>

## ▶️ Ejecutar la aplicación

Desde la raíz del proyecto, ejecuta el archivo principal de Flask:

```bash
python app/run.py
```

## 📱 Interfaz de usuario

La aplicación utiliza **TailwindCSS** para una interfaz limpia y moderna. Las vistas están optimizadas para dispositivos móviles.


## Requerimientos Funcionales

### Frontend:

- **Panel de usuario** para registrar pagos y consultar su historial.
- **Sección para enviar reclamos** con evidencia (texto, imágenes).
- **Notificaciones de mantenimiento programado** y recordatorio de pagos.
- **Dashboard administrativo** para gestionar reportes y reclamos.
- **Gráficos interactivos** sobre ingresos y gastos residenciales.

### Backend:

- **Base de datos** para pagos, reclamos, reportes y usuarios.
- **Algoritmo** para calcular cuotas mensuales y generar recibos automáticos.
- **Sistema de estadística** para evaluar el estado financiero de la comunidad.
- **Gestión de roles** (administrador, residente).


## Tecnologías implementadas en el Proyecto

### Frontend:

- **Tecnologías base:**

  - HTML
  - CSS
  - JavaScript
- **Librerías y herramientas:**

  - Tailwind CSS
  - Flowbite
  - DaisyUI
  - Google Fonts
  - Google Icons
  - Heroicons
  - SailboatUI
  - MerakiUI
  - Alpine.js
  - Undraw
  - Jinja2

### Backend:

- **Tecnologías base:**

  - Flask (Python)
  - MySQL
- **Librerías y Herramientas:**

  - Bcrypt
  - Mysql-connector
  - Gmail (API)
