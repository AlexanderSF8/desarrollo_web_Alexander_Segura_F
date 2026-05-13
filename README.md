# Tarea 1: Sistema de Registro Comunidad DCC

Este proyecto consiste en una aplicación web estática para el registro y visualización de miembros de la comunidad del Departamento de Ciencias de la Computación. Esta primera parte se enfoca en la experiencia de usuario (UX), validaciones robustas en el cliente y un diseño responsivo que cumpla con los estándares.

## 🛠️ Tecnologías Utilizadas

* **Bootstrap 5:** Framework principal para el sistema de grillas, componentes (cards, badges, botones) y utilidades de espaciado.
* **CSS Personalizado (`styles.css`):** Archivo dedicado para particularidades estéticas que van más allá del framework, como el centrado de la portada, sombras personalizadas y el ajuste de imágenes mediante `object-fit`.
* **JavaScript (Vanilla):** Lógica pura para la manipulación dinámica del DOM y validaciones sin dependencias externas.

## 📂 Estructura del Proyecto

### 1. Portada e Inicio (`index.html`)
Punto de entrada con navegación clara hacia las tres secciones principales: registro, listado de miembros y estadísticas.

### 2. Flujo de Registro (`register.html` & `activities.html`)
* **Navegación Intuitiva:** Se implementaron botones de "Volver" y "Continuar" con jerarquía visual (primario y secundario) para guiar al usuario.
* **Validaciones Proactivas:** Uso del evento `submit` y `event.preventDefault()` para interceptar errores antes del envío. Se validan formatos de correo, teléfonos chilenos y campos obligatorios.
* **Persistencia Local:** Uso de `localStorage` para transferir la categoría del usuario entre páginas, permitiendo una experiencia personalizada.
* **Formularios Dinámicos:** En `activities.html`, el formulario muestra secciones específicas (Estudiante, Académico o Funcionario) según el rol detectado, optimizando el espacio mediante la clase `d-none`.

### 3. Directorio de Miembros (`list.html`)
Una interfaz de búsqueda avanzada que permite explorar la comunidad:
* **Buscador Global:** Filtra por nombre, correo o Telegram en tiempo real.
* **Filtros y Orden:** Clasificación por rol y ordenamiento alfabético inteligente (A-Z / Z-A).
* **Paginación Lógica:** Sistema dinámico que divide el contenido para mejorar la legibilidad y el rendimiento.

### 4. Estadísticas (`statistics.html`)
Dashboard con métricas clave del sistema:
* **KPI Cards:** Resumen de registros, actividades y horas promedio.
* **Gráficos:** Visualizaciones de la composición de la comunidad y tipos de actividades realizadas.

------------------------------------------------------------------------------------------------------

# Tarea 2: Arquitectura Back-End, ORM y Base de Datos Relacional

En esta segunda iteración, el proyecto evolucionó de una maqueta estática (Front-End) a una aplicación web transaccional completa (Full-Stack). Se implementó un servidor en Python con Flask y se estructuró una base de datos relacional en MySQL, utilizando SQLAlchemy como capa de abstracción (ORM) para garantizar la seguridad, escalabilidad y consistencia de los datos de la comunidad.

### 📂 Arquitectura de Archivos Clave

La lógica del servidor se separó en módulos funcionales para mantener un código limpio y mantenible:

* **`app.py` (El Controlador Principal):** Actúa como el corazón de la aplicación. Define los *endpoints* (rutas HTTP), orquesta la comunicación entre los formularios del usuario y la base de datos, administra el contexto de las sesiones de SQLAlchemy, y maneja el sistema de redirecciones y mensajería global (Flask `flash`).
* **Directorio `database/`:**
    * **`models.py`:** Contiene el mapeo objeto-relacional (ORM). Aquí se definieron las clases `Miembro`, `Actividad`, `Foto`, `Comuna` y `Region`. Se configuraron meticulosamente las llaves foráneas (`ForeignKey`) y las relaciones inversas (`relationship`). Un punto crítico del diseño fue la implementación de reglas de eliminación en cascada (`cascade="all, delete-orphan"`) desde el Miembro hasta las Fotos, delegando la responsabilidad de la integridad referencial al motor de base de datos.
* **Scripts de Mantenimiento (`reset_db.py` y `.sql`):** Herramientas desarrolladas para la automatización del entorno. Permiten purgar el esquema de la base de datos, recrear las tablas con las reglas actualizadas del ORM y repoblar el catálogo maestro (Regiones y Comunas) sin necesidad de intervenciones manuales en el gestor de BD.

### 🔄 Flujos Lógicos del Sistema

El comportamiento dinámico de la aplicación se dividió en tres flujos principales:

#### 1. Flujo de Registro Secuencial (Miembro ➔ Actividad)
Se abandonó el uso temporal de `localStorage` de la Tarea 1 en favor de un manejo de estado seguro en el servidor.
* **Fase 1 (Miembro):** Al enviar el formulario en `/register`, `app.py` captura los datos mediante `request.form`. Se realiza una validación estricta (Doble Capa: Front-End y Back-End sincronizados). Si la transacción es exitosa, se hace un `commit` en la base de datos y se redirige al usuario a `/activities`, pasando el ID del miembro recién creado como referencia de sesión.
* **Fase 2 (Actividad):** En la ruta `/activities`, el sistema asocia la nueva actividad al miembro correspondiente. Para manejar la variabilidad de datos según el rol (Estudiante, Académico, Funcionario), se implementó evaluación de corto circuito (`request.form.get('campo') or None`). Esto intercepta los strings vacíos (`''`) enviados por HTML y los transforma en valores `NULL` nativos de Python, evitando errores de tipado estricto en columnas `Integer` de MySQL.

#### 2. Flujo de Directorio y Listado (`/list`)
La ruta de listado consulta la totalidad de los miembros registrados junto con sus actividades asociadas. 
* Para evitar errores de renderizado cuando los campos categóricos (como el cargo o los ramos) vienen vacíos (comportamiento esperado al ser `nullable=True`), se implementó lógica defensiva tanto en Python como en el motor de plantillas Jinja2, reemplazando dinámicamente los valores `NULL` por un string predeterminado ('N/A').

#### 3. Flujo de Portada y Optimización de Consultas (`/` Index)
Para la página de inicio, se diseñó una tabla dinámica que proyecta los últimos 5 miembros registrados en la comunidad.
* **Manejo Temporal:** Se delegó la creación de marcas de tiempo al motor de base de datos mediante `server_default=func.now()` en el modelo `Miembro`, asegurando la precisión de la hora de registro (`fecha_registro`).
* **Optimización ORM (`joinedload`):** Para proyectar la "Región" a la que pertenece el miembro, la consulta debe atravesar dos relaciones (`Miembro` -> `Comuna` -> `Region`). Para evitar el problema clásico de rendimiento de *N+1 consultas* (Lazy Loading), se implementó `joinedload` en `app.py`. Esto instruye a SQLAlchemy para que realice un *JOIN* subyacente y recupere toda la jerarquía geográfica en una única y eficiente petición a la base de datos, entregando un objeto listo para ser consumido por Jinja2.