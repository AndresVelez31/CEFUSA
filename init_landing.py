"""
Script para inicializar la página landing con datos de prueba.
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CEFUSA.settings')
django.setup()

from Applications.core.models import LandingPage, LandingSlide

def init_landing():
    # Crear o actualizar página principal
    page, created = LandingPage.objects.get_or_create(pk=1)
    page.title = 'Bienvenido a CEFUSA'
    page.subtitle = 'Tu viaje hacia la excelencia futbolística comienza aquí.'
    page.save()
    
    print(f"✓ Página principal {'creada' if created else 'actualizada'}")
    
    # Crear slides de ejemplo
    slides_data = [
        {
            'section': 'news',
            'title': 'CEFUSA Anuncia Nueva Instalación de Entrenamiento',
            'content': 'CEFUSA se complace en anunciar la apertura de nuestra nueva instalación de entrenamiento de última generación. Esta instalación proporcionará a nuestros atletas los mejores recursos para desarrollar sus habilidades y alcanzar su máximo potencial.',
            'order': 1,
        },
        {
            'section': 'news',
            'title': 'CEFUSA U17 Campeones del Campeonato Nacional',
            'content': '¡Felicitaciones al equipo CEFUSA U17 por ganar el Campeonato Nacional! Su arduo trabajo y dedicación a lo largo de la temporada han dado sus frutos, y estamos increíblemente orgullosos de su logro.',
            'order': 2,
        },
    ]
    
    for slide_data in slides_data:
        slide, created = LandingSlide.objects.get_or_create(
            page=page,
            section=slide_data['section'],
            title=slide_data['title'],
            defaults={
                'content': slide_data['content'],
                'order': slide_data['order'],
                'active': True,
            }
        )
        if not created:
            slide.content = slide_data['content']
            slide.order = slide_data['order']
            slide.active = True
            slide.save()
        
        print(f"✓ Slide {'creado' if created else 'actualizado'}: {slide.title}")
    
    print("\n✅ Inicialización completada!")

if __name__ == '__main__':
    init_landing()
