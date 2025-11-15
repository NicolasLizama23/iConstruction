# iConstruction (Django + MySQL XAMPP)
Módulos: Bodega (materiales, herramientas, movimientos y asignaciones), Proyectos y Actividades (avance), Reportes (CSV y Excel).

## Instalación (Windows + XAMPP)
1) Instala Python 3.11+ y Git.
2) Abre XAMPP Control Panel y levanta **Apache** y **MySQL**.
3) Crea base de datos:
   - Abre `http://localhost/phpmyadmin` → pestaña SQL:
   ```sql
   CREATE DATABASE iconstruction CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
   ```
4) Clona el proyecto o copia esta carpeta.
5) Crea y activa venv:
   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
   Si mysqlclient falla, instala compiladores de Visual Studio Build Tools o usa `pip install --only-binary :all: mysqlclient` si procede.
6) Copia `.env.example` a `.env` y ajusta credenciales.
7) Migra y crea superusuario:
   ```powershell
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```
8) Entra a `http://127.0.0.1:8000/` (login requerido).

## Casos de Prueba (resumen)
- Crear material, registrar ingreso y salida; verificar stock actualizado.
- Crear herramienta, asignar a usuario y luego registrar devolución.
- Crear proyecto, actividad y registro de avance (log); revisar % y estado.
- Descargar reportes CSV y Excel de inventario y actividades.
- Ejecutar pruebas de rendimiento con `python performance_test.py`.
- Poblar datos de prueba con `python populate_data.py`.

## Seguridad
- Autenticación por Django auth; limitar permisos vía admin según perfiles.
- Validación de entradas por formularios; CSRF activo.

## Estructura
- `inventory`: Materiales, Herramientas, Movimientos, Asignaciones.
- `activities`: Proyectos, Actividades, Logs de avance.
- `reports`: Exportación CSV y Excel.
- `core`: Panel de control (dashboard).
- `populate_data.py`: Script para poblar datos de prueba (250 materiales, 50 herramientas, 1000 movimientos, 20 proyectos).
- `performance_test.py`: Script de pruebas de rendimiento (listados, exportaciones CSV).

## Despliegue
- Configurar `ALLOWED_HOSTS` y `DEBUG=0` en `.env`.
- Servir `staticfiles` con `collectstatic` y un servidor WSGI (gunicorn/uwsgi + Nginx).
