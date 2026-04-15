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
