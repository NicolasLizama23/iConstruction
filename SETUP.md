# 🏗️ iConstruction Project - Guía de Configuración

Guía completa para configurar y ejecutar el proyecto iConstruction en tu máquina.

## 📋 Requisitos Previos

- **Python 3.13+** instalado
- **XAMPP** (o MySQL) instalado y corriendo
- **Git** configurado
- **pip** y **virtualenv** (o conda)

---

## 🚀 Instalación y Configuración

### 1️⃣ Clonar el Repositorio

```powershell
git clone https://github.com/NicolasLizama23/Ev03ProyectoIntegrado.git
cd Ev03ProyectoIntegrado
```

### 2️⃣ Crear y Activar Entorno Virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3️⃣ Instalar Dependencias

```powershell
pip install -r requirements.txt
```

### 4️⃣ Configurar Base de Datos MySQL

**Verificar que XAMPP está corriendo:**
- Abrir XAMPP Control Panel
- Asegurarse de que **MySQL** esté corriendo (debe estar en verde)

**Crear la base de datos:**
```sql
CREATE DATABASE iconstruction CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

O desde PowerShell (si `mysql.exe` está en PATH):
```powershell
mysql -u root -e "CREATE DATABASE IF NOT EXISTS iconstruction CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

### 5️⃣ Aplicar Migraciones

```powershell
python manage.py migrate
```

### 6️⃣ Crear Usuarios y Grupos (Importante ⚠️)

```powershell
python manage.py shell -c "exec(open('setup_users.py').read())"
```

O alternativamente:
```powershell
python create_groups.py
```

---

## 👥 Usuarios Disponibles

Todos los usuarios usan la contraseña: **`hola1234`**

| Usuario | Rol | Descripción |
|---------|-----|-------------|
| `admin` | Administrador | Acceso total al sistema |
| `bodeguero` | Bodeguero | Gestión de inventario y materiales |
| `planificador` | Planificador | Planificación de proyectos y actividades |
| `supervisor` | Supervisor | Visualización y supervisión general |
| `analista` | Analista | Análisis de reportes y datos |
| `operario` | Operario | Acceso básico para operarios |

---

## ▶️ Ejecutar el Servidor

```powershell
python manage.py runserver 127.0.0.1:8000
```

O con puerto personalizado:
```powershell
python manage.py runserver 0.0.0.0:8080
```

El servidor estará disponible en:
- **Dashboard:** http://127.0.0.1:8000/dashboard/
- **Login:** http://127.0.0.1:8000/accounts/login/
- **Admin:** http://127.0.0.1:8000/admin/

---

## 🔧 Solución de Problemas

### ❌ Error: "Can't connect to MySQL server"

**Solución:**
1. Verificar que XAMPP está corriendo
2. Verificar que MySQL esté en verde en XAMPP Control Panel
3. Comprobar puerto (por defecto 3306)
4. Verificar credenciales en `iconstruction_project/settings.py`

```python
# settings.py - líneas 46-53
DB_NAME = 'iconstruction'
DB_USER = 'root'
DB_PASSWORD = ''  # Por defecto está vacío en XAMPP
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
```

### ❌ Error: "MariaDB 10.5 or later is required"

**Solución (temporal):**
Cambiar a SQLite en desarrollo editando `iconstruction_project/settings.py`:

```python
# Comentar MySQL
# DATABASES = { ... }

# Descomentar SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Luego ejecutar migraciones nuevamente.

### ❌ Error: "Unknown database 'iconstruction'"

**Solución:**
Ejecutar comando SQL para crear la BD antes de las migraciones:
```bash
mysql -u root -e "CREATE DATABASE IF NOT EXISTS iconstruction CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

---

## 📁 Estructura del Proyecto

```
Ev03ProyectoIntegrado/
├── manage.py                          # CLI de Django
├── requirements.txt                   # Dependencias Python
├── setup_users.py                     # Script para crear usuarios
├── create_groups.py                   # Script para crear grupos
├── iconstruction_project/
│   ├── settings.py                    # Configuración Django
│   ├── urls.py                        # URLs principales
│   └── wsgi.py                        # WSGI para producción
├── core/                              # App principal (dashboard)
│   ├── views.py
│   ├── urls.py
│   └── migrations/
├── inventory/                         # Gestión de inventario
│   ├── models.py                      # Material, Tool, MaterialMovement
│   ├── forms.py
│   ├── views.py
│   └── migrations/
├── activities/                        # Proyectos y actividades
│   ├── models.py                      # Project, Activity
│   ├── forms.py
│   ├── views.py
│   └── migrations/
├── reports/                           # Reportes
│   ├── views.py
│   └── urls.py
├── templates/                         # Plantillas HTML
│   ├── base.html                      # Template base
│   ├── core/
│   ├── inventory/
│   ├── activities/
│   └── registration/
└── static/                            # CSS, JS, imágenes
    └── css/style.css
```

---

## 🧪 Pruebas de Rendimiento

El proyecto incluye script de pruebas:

```powershell
python performance_test.py
```

Y población de datos de prueba:

```powershell
python populate_data.py
```

---

## 📝 Desarrollo

### Crear nuevas migraciones después de cambios en modelos

```powershell
python manage.py makemigrations
python manage.py migrate
```

### Crear superusuario adicional

```powershell
python manage.py createsuperuser
```

### Recolectar archivos estáticos

```powershell
python manage.py collectstatic
```

---

## 🔐 Seguridad para Producción

Antes de deployar a producción:

1. Cambiar `DEBUG = False` en `settings.py`
2. Generar nueva `SECRET_KEY`
3. Configurar `ALLOWED_HOSTS`
4. Usar contraseñas seguras (no `hola1234`)
5. Configurar HTTPS
6. Usar gestor de secretos para credenciales

---

## 📞 Contacto y Soporte

Para reportar problemas o hacer preguntas, abrir un **Issue** en GitHub.

---

**Última actualización:** 3 de diciembre de 2025
**Versión:** 1.0
