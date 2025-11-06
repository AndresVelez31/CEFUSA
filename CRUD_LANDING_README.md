# CRUD de Gestión de Contenido - Landing Page CEFUSA

## 📋 Descripción

Sistema completo de administración (CRUD) para gestionar el contenido dinámico de la página de inicio (`cefusa_landing.html`). Permite editar títulos, subtítulos, imágenes y slides de las secciones de Noticias, Torneos y Partidos.

## 🎯 Características

### Modelos Creados

1. **LandingPage**: Configuración general de la página
   - `title`: Título principal
   - `subtitle`: Subtítulo descriptivo
   - `background`: Imagen de fondo (opcional)
   - `updated_at`: Fecha de última actualización

2. **LandingSlide**: Contenido de cada slide del carrusel
   - `section`: Sección (Noticias, Torneos, Partidos)
   - `title`: Título del slide
   - `subtitle`: Subtítulo
   - `content`: Contenido descriptivo
   - `image`: Imagen del slide
   - `order`: Orden de visualización
   - `active`: Estado activo/inactivo

## 🚀 Acceso al Sistema

### URLs Disponibles

```
/manage-home/                           # Lista y gestión general
/manage-home/edit/                      # Editar página principal
/manage-home/slides/add/                # Crear nuevo slide
/manage-home/slides/<id>/edit/          # Editar slide existente
/manage-home/slides/<id>/delete/        # Eliminar slide
```

### Requisitos de Acceso

- Usuario autenticado con permisos de **staff** (administrador)
- Acceso desde el panel de administración o directamente por URL

## 📖 Guía de Uso

### 1. Acceder a la Gestión

Después de iniciar sesión como administrador, accede a:
```
http://127.0.0.1:8000/manage-home/
```

### 2. Editar Configuración General

- Haz clic en **"Editar página"**
- Modifica el título, subtítulo y/o imagen de fondo
- Guarda los cambios

### 3. Gestionar Slides

#### Crear Nuevo Slide
1. Clic en **"Nuevo slide"**
2. Completa los campos:
   - **Sección**: Elige entre Noticias, Torneos o Partidos
   - **Título**: Título del contenido
   - **Subtítulo**: (Opcional) Subtítulo adicional
   - **Contenido**: Descripción detallada
   - **Imagen**: Sube una imagen (opcional)
   - **Orden**: Número para ordenar la visualización
   - **Activo**: Marca si debe mostrarse en la página
3. Guarda

#### Editar Slide Existente
1. En la tabla de slides, clic en **"Editar"**
2. Modifica los campos necesarios
3. Guarda los cambios

#### Eliminar Slide
1. En la tabla de slides, clic en **"Eliminar"**
2. Confirma la eliminación

### 4. Administración Avanzada (Django Admin)

También puedes gestionar el contenido desde el panel de Django Admin:
```
http://127.0.0.1:8000/admin/
```

- **Landing Pages**: Gestión con inline de slides
- **Landing Slides**: Filtrado por sección y estado activo

## 🛠️ Configuración Técnica

### Archivos Modificados/Creados

```
Applications/core/
├── models.py              # Modelos LandingPage y LandingSlide
├── forms.py               # Formularios para CRUD
├── views.py               # Vistas de gestión (manage_landing, edit_*, create_*, delete_*)
├── urls.py                # Rutas del CRUD
├── admin.py               # Registro en Django Admin
└── templates/
    ├── home_content_management.html   # Lista de contenido
    ├── edit_home_content.html         # Formulario de edición
    └── cefusa_landing.html            # Landing actualizada (dinámica)

CEFUSA/
├── settings.py            # MEDIA_URL y MEDIA_ROOT añadidos
└── urls.py                # Configuración para servir archivos media

migrations/
└── 0003_initial.py        # Migración con LandingPage y LandingSlide
```

### Configuración de Media

En `CEFUSA/settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Las imágenes subidas se guardan en:
- Fondo de página: `media/landing/`
- Imágenes de slides: `media/landing/slides/`

## 🔧 Comandos Útiles

### Inicializar con Datos de Ejemplo
```powershell
python init_landing.py
```

### Crear Migraciones y Aplicar
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Iniciar Servidor de Desarrollo
```powershell
python manage.py runserver
```

## 📱 Visualización en la Página Pública

La página landing (`/`) ahora carga contenido dinámicamente:
- El título y subtítulo se obtienen del modelo `LandingPage`
- Los slides de la sección "Noticias" se cargan desde `LandingSlide`
- Solo se muestran slides con `active=True`
- Las imágenes se cargan desde los archivos subidos o placeholders

## 🔐 Permisos y Seguridad

- Solo usuarios con `is_staff=True` pueden acceder al CRUD
- Las vistas verifican permisos con `@login_required` y `user.is_staff`
- Archivos media se sirven solo en modo DEBUG
- En producción, configura un servidor web (nginx/Apache) para servir media

## 📝 Notas Adicionales

### Limitaciones Actuales
- Las secciones de "Torneos" y "Partidos" aún usan contenido estático en la plantilla
- Para hacerlas dinámicas, replicar la lógica usada en "Noticias"

### Próximas Mejoras Sugeridas
1. Hacer dinámicas todas las secciones del carrusel
2. Agregar editor WYSIWYG para contenido
3. Redimensionamiento automático de imágenes
4. Previsualización antes de publicar
5. Versionado de contenido

## 🐛 Solución de Problemas

### Las imágenes no se muestran
- Verifica que `DEBUG=True` en `settings.py`
- Asegúrate de que la carpeta `media/` existe
- Revisa que `MEDIA_URL` y `MEDIA_ROOT` estén configurados

### Error "cannot import name 'user_can_access_home_content'"
- Ya corregido: se eliminó la importación inexistente de `utils.py`

### Migración no se aplica
```powershell
python manage.py makemigrations core
python manage.py migrate core
```

## ✅ Estado del Proyecto

- ✅ Modelos creados y migrados
- ✅ Formularios implementados
- ✅ Vistas CRUD funcionales
- ✅ Templates de gestión creados
- ✅ URLs configuradas
- ✅ Admin registrado
- ✅ Integración dinámica en landing (sección Noticias)
- ✅ Script de inicialización
- ✅ Servidor funcionando

---

**Creado**: 6 de noviembre de 2025  
**Versión**: 1.0.0  
**Proyecto**: CEFUSA - Centro de Formación de Fútbol
