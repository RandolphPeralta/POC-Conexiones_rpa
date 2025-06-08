# Consulta de Autorizaciones 

Este proyecto automatiza la consulta de autorizaciones en la plataforma web de SAVIA Salud EPS utilizando **Selenium** y **Python**. El resultado de cada consulta se guarda como archivo `.json`.

## 🧩 Estructura del Proyecto

```
.
├── main.py
├── .env
├── autorizaciones/
│   └── datos_autorizacion_<numero>.json
├── services/
│   ├── login_service.py
│   └── autorizacion_service.py
```

main.py: Script principal que ejecuta la automatización.

services/login_service.py: Contiene la lógica de inicio de sesión.

services/autorizacion_service.py: Contiene la lógica para consultar y guardar los datos de autorización.

autorizaciones/: Carpeta donde se guardan los archivos JSON generados por cada consulta.

## ⚙️ Requisitos
Python 3.8+

Google Chrome

ChromeDriver compatible con tu versión de Chrome

## Instalar dependencias
```
pip install -r requirements.txt
```

Contenido sugerido para requirements.txt:
```
selenium
python-dotenv
```

## 🔐 Variables de Entorno
Crea un archivo .env con las siguientes variables:

```
USUARIO_SAVIA=tu_usuario
CONTRASENA_SAVIA=tu_contraseña
```

## 🚀 Ejecución
Ejecuta el script principal:

```
python main.py
```
