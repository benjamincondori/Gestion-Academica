# Blog-Posts
# Requerimientos e Instalación

Este proyecto utiliza **Python**. Asegúrate de tenerlo instalado antes de comenzar.

## 1. Instalar el entorno virtual

Para crear un entorno virtual:

```bash
python -m venv .venv
```

## 2. Activar el entorno virtual

Dependiendo de la terminal que utilices, activa el entorno virtual con uno de los siguientes comandos:

### Git Bash:

```bash
source .venv/Scripts/activate
```

### Terminal de VSCode (Windows):

```bash
.\venv\Scripts\activate
```

### Desactivar el entorno virtual

Para desactivar el entorno virtual en cualquier terminal:

```bash
deactivate
```

## 3. Instalar Flask

Con el entorno virtual activado, instala Flask:

```bash
pip install flask
```

## 4. Ejecutar la aplicación Flask

Para ejecutar la aplicación:

```bash
flask --app main --debug run --host=0.0.0.0
```

## 5. Instalar las dependencias

Con el entorno virtual activado y desde la raíz del proyecto, instala todas las dependencias:

```bash
pip install -r requirements.txt
```

Si no tienes el archivo `requirements.txt`, puedes instalar manualmente las dependencias con los siguientes comandos:

```bash
pip install flask_sqlalchemy
pip install psycopg2
pip install python-dotenv
pip install gunicorn
pip install Flask-WTF
pip install email-validator
pip install Faker
```

## 6. Ejecutar comandos CLI

Para ejecutar los seeders, utiliza el siguiente comando:

### Cargar datos seed en la base de datos:
```bash
flask seed
```

Inicializa la base de datos con datos de prueba.



Este archivo `README.md` está estructurado para seguir las convenciones estándar y proporcionar una guía clara sobre cómo configurar y ejecutar el proyecto.
