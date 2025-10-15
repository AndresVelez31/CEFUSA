# Instalación de Fuentes Personalizadas - CEFUSA Branding

## 🎨 Fuentes Requeridas

Para que el branding de CEFUSA se vea correctamente, necesitas instalar las siguientes fuentes:

### 📝 **Almaq W01 Rough** (Títulos)
- **Uso**: Títulos principales (H1, H2)
- **Ubicación**: `/Applications/core/static/fonts/`
- **Archivos necesarios**:
  - `AlmaqW01-Rough.woff2` (preferido)
  - `AlmaqW01-Rough.woff` (respaldo)

### 📝 **Bricolage Grotesque** (Subtítulos)
- **Uso**: Subtítulos (H3, H4, H5, H6)
- **Fuente**: Google Fonts (se carga automáticamente)
- **No requiere instalación manual**

## 🚀 Pasos de Instalación

### 1. Obtener la fuente Almaq W01 Rough

La fuente "Almaq W01 Rough" es una fuente comercial. Puedes obtenerla de:
- **Monotype**: https://www.monotype.com/
- **MyFonts**: https://www.myfonts.com/
- **Adobe Fonts** (si tienes suscripción Creative Cloud)

### 2. Convertir la fuente a formato web

Si tienes la fuente en formato `.otf` o `.ttf`, conviértela usando:
- **Convertidor online**: https://convertio.co/es/otf-woff2/
- **Fontello**: http://fontello.com/
- **Transfonter**: https://transfonter.org/

### 3. Colocar los archivos

Coloca los archivos de fuente en:
```
Applications/core/static/fonts/
├── AlmaqW01-Rough.woff2
└── AlmaqW01-Rough.woff
```

### 4. Verificar la instalación

1. Ejecuta el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

2. Visita la página principal y verifica que los títulos usen la fuente correcta

## 🔧 Configuración Actual

La aplicación está configurada para:

- **Cargar automáticamente** la fuente desde `/static/fonts/`
- **Usar Arial Black como respaldo** si la fuente no está disponible
- **Aplicar la fuente** automáticamente a elementos con clase `.font-title`

## 🎯 Uso en Templates

```html
<!-- Cargar el CSS de branding -->
<link rel="stylesheet" href="{% static 'css/branding-fonts.css' %}">

<!-- Usar en títulos -->
<h1 class="font-title">Título Principal</h1>
<h2 class="font-title">Título Secundario</h2>

<!-- Usar en subtítulos -->
<h3 class="font-subtitle">Subtítulo</h3>
```

## ⚠️ Notas Importantes

1. **Licencia**: Asegúrate de tener los derechos de uso de la fuente Almaq W01 Rough
2. **Rendimiento**: Los archivos WOFF2 son más pequeños y se cargan más rápido
3. **Respaldo**: Siempre incluye fuentes de respaldo (Arial Black, sans-serif)
4. **Derechos de autor**: No incluyas archivos de fuentes comerciales en repositorios públicos

## 🐛 Solución de Problemas

### La fuente no se muestra
1. Verifica que los archivos estén en `/static/fonts/`
2. Ejecuta `python manage.py collectstatic`
3. Revisa la consola del navegador para errores de carga

### Fuentes se ven diferentes en otros dispositivos
1. Asegúrate de incluir los archivos WOFF/WOFF2
2. Verifica que las fuentes de respaldo estén configuradas
3. Usa `font-display: swap` para mejor rendimiento

## 📁 Estructura de Archivos

```
Applications/
└── core/
    └── static/
        ├── css/
        │   └── branding-fonts.css
        └── fonts/
            ├── AlmaqW01-Rough.woff2
            └── AlmaqW01-Rough.woff
```