
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

Abre tu gestor de base de datos MySQL y crea una base de datos. Puedes llamarla como prefieras, por ejemplo:

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
