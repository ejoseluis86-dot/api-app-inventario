
```markdown
# ⚙️ API - App de Inventario

¡Bienvenido al repositorio de la **API de la App de Inventario**! Este proyecto es el backend encargado de procesar la lógica de negocio, gestionar la base de datos y proveer los servicios REST necesarios para que la aplicación móvil (Flutter) funcione correctamente a través de peticiones HTTP.

---

## 📋 Descripción del Proyecto

Esta API actúa como el núcleo del sistema de inventario. Maneja de forma centralizada la persistencia de datos y las operaciones CRUD para:
*   **Insumos:** Gestión y control de Insumos (materias primas).
*   **Productos:** Registro de Productos creados a partir de los Insumos listos para la Entrega.
*   **Pedidos:** Control y flujo de pedios. Consulta del Consumo Real de los insumos utilizado en cada pedido entregado

---

## 🛠️ Arquitectura y Estructura

El backend está desarrollado sobre **Django** (Python) y mantiene una estructura limpia dividida por aplicaciones/módulos:

```text
api-app-inventario/
├── Insumos/                 # Módulo/App encargada de la lógica de insumos y recursos
├── config/                  # Configuración global del proyecto Django (settings, urls, etc.)
├── manage.py                # Script de gestión de comandos de Django
└── .gitignore               # Archivos omitidos en el control de versiones

```

---

## ⚙️ Requisitos Previos

Asegúrate de tener instalado lo siguiente en tu servidor o entorno local:

* **Python 3.x**
* **Pip** (Administrador de paquetes de Python)
* **Virtualenv** (Recomendado para aislamiento de dependencias)

---

## 💻 Instalación y Configuración

Sigue estos pasos para levantar el entorno de desarrollo local:

1. **Clona este repositorio:**
```bash
git clone [https://github.com/ejoseluis86-dot/api-app-inventario/api-app-inventario.git](https://github.com/ejoseluis86-dot/api-app-inventario/api-app-inventario.git)
cd api-app-inventario

```


2. **Crea y activa un entorno virtual:**
* En Windows:
```bash
python -m venv venv
.\venv\Scripts\activate

```


* En macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate

```




3. **Instala las dependencias necesarias:**
*(Asegúrate de crear tu archivo `requirements.txt` o instalar Django manualmente si aún no lo has congelado)*
```bash
pip install django djangorestframework
# o bien: pip install -r requirements.txt

```


4. **Aplica las migraciones de la base de datos:**
```bash
python manage.py migrate

```


5. **Inicia el servidor de desarrollo:**
```bash
python manage.py runserver

```


Por defecto, la API estará disponible en `http://127.0.0.1:8000/`.
**pero debes  iniciar el servidor en 0.0.0.0:8000** 
```bash
python manage.py runserver 0.0.0.0:8000

```

---

## 🔄 Integración con la App Móvil

Para que la aplicación de Flutter pueda consumir estos servicios:

1. Asegúrate de que tanto el servidor de la API como el emulador/dispositivo móvil estén en la misma red.
2. Configura la URL base en el archivo de servicios (`services/`) de tu app de Flutter apuntando a la IP de tu servidor local (ej. `http://192.168.X.X:8000/api/`).

---

## 🤝 Contribuciones

Si deseas agregar nuevos endpoints o mejorar la lógica actual:

1. Haz un *Fork* del proyecto.
2. Crea una rama para tu feature (`git checkout -b feature/NuevoEndpoint`).
3. Sube tus cambios (`git commit -m 'Añade endpoint de pedidos'`).
4. Haz un *Push* (`git push origin feature/NuevoEndpoint`).
5. Abre un *Pull Request*.

```

```
