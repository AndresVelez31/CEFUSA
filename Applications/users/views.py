from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
# Logic behind users templates (real function)
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from datetime import date, timedelta

from .models import Acudiente, Jugador
from .forms import AcudienteForm, JugadorForm

# Create your views here.

def usersManagement(request): # Basic research
    # Obtener parámetros de filtro
    search = request.GET.get('search', '')
    tipo_doc = request.GET.get('tipo_doc', '')
    ciudad = request.GET.get('ciudad', '')
    tipo_usuario = request.GET.get('tipo_usuario', '')
    
    # Filtrar acudientes
    acudientes = Acudiente.objects.all() #Internal function of django that obtains all records from the Acudiente table

    #Filtro de Busqueda General
    # It works for all this paraemter withouth taking into account MAY o MIN
    if search:  
        acudientes = acudientes.filter(
            Q(nombre__icontains=search) |
            Q(apellidos__icontains=search) |
            Q(identificacion__icontains=search) |
            Q(correo__icontains=search) |
            Q(ciudad__icontains=search) |
            Q(telefono__icontains=search) |
            Q(direccion__icontains=search) |
            Q(tipo_regimen__icontains=search) |
            Q(tipo_doc__icontains=search)
        )

    #Filtro de Tipo de documento
    if tipo_doc:
        acudientes = acudientes.filter(tipo_doc=tipo_doc)
    
    #Filtro de Ciudad
    if ciudad:
        acudientes = acudientes.filter(ciudad=ciudad)
    
    # Si solo se quieren jugadores, vaciar acudientes
    if tipo_usuario == 'jugadores':
        acudientes = Acudiente.objects.none()
    
    # Filtrar jugadores
    jugadores = Jugador.objects.select_related('acudiente').all()
    
    if search:
        jugadores = jugadores.filter(
            Q(nombre__icontains=search) |
            Q(apellido__icontains=search) |
            Q(identificacion__icontains=search) |
            Q(acudiente__nombre__icontains=search) |
            Q(acudiente__apellidos__icontains=search) |
            Q(institucion_educativa__icontains=search)
        )
    
    if tipo_doc:
        jugadores = jugadores.filter(tipo_doc=tipo_doc)
    
    if ciudad:
        jugadores = jugadores.filter(ciudad=ciudad)
    
    # Si solo se quieren acudientes, vaciar jugadores
    if tipo_usuario == 'acudientes':
        jugadores = Jugador.objects.none()
    
    # Obtener ciudades disponibles para el filtro
    ciudades_acudientes = set(Acudiente.objects.values_list('ciudad', flat=True).distinct())
    ciudades_jugadores = set(Jugador.objects.values_list('ciudad', flat=True).distinct())
    ciudades_disponibles = sorted(ciudades_acudientes.union(ciudades_jugadores))
    
    # Orden que queremos usar (desde el TextChoices)
    orden_tipodoc = [opcion.label for opcion in Acudiente.TipoDocumento]

    # Obtener tipos de documentos desde ambos modelos
    tipos_acudientes = set(Acudiente.objects.values_list('tipo_doc', flat=True).distinct())
    tipos_jugadores = set(Jugador.objects.values_list('tipo_doc', flat=True).distinct())

    # Unir los tipos y pasarlos a lista
    tipos_doc_en_bd = list(tipos_acudientes.union(tipos_jugadores))

    # Crear mapa de índices para orden personalizado
    index_map = {label: idx for idx, label in enumerate(orden_tipodoc)}

    # Ordenar según el orden definido, dejando desconocidos al final
    tipos_doc_en_bd.sort(key=lambda x: index_map.get(x, len(index_map)))
    
    context = {
        'acudientes': acudientes,
        'jugadores': jugadores,
        'ciudades_disponibles': ciudades_disponibles,
        'tipos_doc_en_bd': tipos_doc_en_bd
    }
    return render(request, 'index.html', context)

def busqueda_avanzada(request): # Advanced search view

    """Vista para búsqueda avanzada con filtros específicos"""
    
    # Parámetros básicos
    search = request.GET.get('search', '')
    tipo_usuario = request.GET.get('tipo_usuario', '')
    ciudad = request.GET.get('ciudad', '')
    tipo_doc = request.GET.get('tipo_doc', '')
    
    # Parámetros específicos de jugadores
    institucion = request.GET.get('institucion', '')
    jornada = request.GET.get('jornada', '')
    rango_edad = request.GET.get('rango_edad', '')
    tiene_enfermedad = request.GET.get('tiene_enfermedad', '')
    
    # Parámetros específicos de acudientes
    correo = request.GET.get('correo', '')
    tipo_regimen = request.GET.get('tipo_regimen', '')

    # Filtrar acudientes
    acudientes = Acudiente.objects.all()
    
    if search:
        acudientes = acudientes.filter(
            Q(nombre__icontains=search) |
            Q(apellidos__icontains=search) |
            Q(identificacion__icontains=search) |
            Q(correo__icontains=search) |
            Q(ciudad__icontains=search) |
            Q(telefono__icontains=search) |
            Q(direccion__icontains=search) |
            Q(tipo_regimen__icontains=search) |
            Q(tipo_doc__icontains=search)
        )
    
    if tipo_doc:
        acudientes = acudientes.filter(tipo_doc=tipo_doc)
 
    if ciudad:
        acudientes = acudientes.filter(ciudad=ciudad)
        
    if correo:
        acudientes = acudientes.filter(correo__icontains=correo)
        
    if tipo_regimen:
        acudientes = acudientes.filter(tipo_regimen=tipo_regimen)
        
    # Obtener orden definido en el TextChoices de tipo_regimen
    orden_regimen = [opcion.label for opcion in Acudiente.TipoRegimen]

    # Obtener valores únicos de tipo_regimen en la base (Acudientes)
    tipo_regimenes_en_bd = list(Acudiente.objects.values_list('tipo_regimen', flat=True).distinct())

    # Crear mapa para ordenar según orden_regimen
    index_map_regimen = {label: idx for idx, label in enumerate(orden_regimen)}

    # Ordenar los valores obtenidos de la BD según el orden definido
    tipo_regimenes_en_bd.sort(key=lambda x: index_map_regimen.get(x, len(index_map_regimen)))
    
    # Si solo se quieren jugadores, vaciar acudientes
    if tipo_usuario == 'jugadores':
        acudientes = Acudiente.objects.none()
    
    # Filtrar jugadores
    jugadores = Jugador.objects.select_related('acudiente').all()
    
    if search:
        jugadores = jugadores.filter(
            Q(nombre__icontains=search) |
            Q(apellido__icontains=search) |
            Q(identificacion__icontains=search) |
            Q(acudiente__nombre__icontains=search) |
            Q(acudiente__apellidos__icontains=search) |
            Q(institucion_educativa__icontains=search)
        )
    
    if tipo_doc:
        jugadores = jugadores.filter(tipo_doc=tipo_doc)
    
    if ciudad:
        jugadores = jugadores.filter(ciudad=ciudad)
        
    if institucion:
        jugadores = jugadores.filter(institucion_educativa__icontains=institucion)
        
    if jornada:
        jugadores = jugadores.filter(jornada_entreno=jornada)
        
    if tiene_enfermedad:
        jugadores = jugadores.filter(tiene_enfermedad=(tiene_enfermedad == 'true'))
    
    
    # Filtro por tipo de doc
    # Orden que queremos usar (desde el TextChoices)
    orden_tipodoc = [opcion.label for opcion in Acudiente.TipoDocumento]

    # Obtener tipos de documentos desde ambos modelos
    tipos_acudientes = set(Acudiente.objects.values_list('tipo_doc', flat=True).distinct())
    tipos_jugadores = set(Jugador.objects.values_list('tipo_doc', flat=True).distinct())

    # Unir los tipos y pasarlos a lista
    tipos_doc_en_bd = list(tipos_acudientes.union(tipos_jugadores))

    # Crear mapa de índices para orden personalizado
    index_map = {label: idx for idx, label in enumerate(orden_tipodoc)}

    # Ordenar según el orden definido, dejando desconocidos al final
    tipos_doc_en_bd.sort(key=lambda x: index_map.get(x, len(index_map)))
    
    # Filtro por rango de edad
    if rango_edad:
        today = date.today()
        if rango_edad == '5-10':
            start_date = today - timedelta(days=10*365)
            end_date = today - timedelta(days=5*365)
        elif rango_edad == '11-15':
            start_date = today - timedelta(days=15*365)
            end_date = today - timedelta(days=11*365)
        elif rango_edad == '16-20':
            start_date = today - timedelta(days=20*365)
            end_date = today - timedelta(days=16*365)
        
        jugadores = jugadores.filter(fecha_nacimiento__range=[start_date, end_date])
    
    # Si solo se quieren acudientes, vaciar jugadores
    if tipo_usuario == 'acudientes':
        jugadores = Jugador.objects.none()
    
    # Agregar edad calculada a jugadores
    for jugador in jugadores:
        jugador.edad = (date.today() - jugador.fecha_nacimiento).days // 365
    
    # Obtener ciudades disponibles
    ciudades_acudientes = set(Acudiente.objects.values_list('ciudad', flat=True).distinct())
    ciudades_jugadores = set(Jugador.objects.values_list('ciudad', flat=True).distinct())
    ciudades_disponibles = sorted(ciudades_acudientes.union(ciudades_jugadores))
    
    total_resultados = acudientes.count() + jugadores.count()
    
    context = {
        'acudientes': acudientes,
        'jugadores': jugadores,
        'ciudades_disponibles': ciudades_disponibles,
        'tipos_doc_en_bd': tipos_doc_en_bd,
        'tipo_regimenes_en_bd': tipo_regimenes_en_bd,
        'total_resultados': total_resultados
    }
    return render(request, 'busqueda_avanzada.html', context)

def get_user_details(request, user_type, user_id):
    """Vista AJAX para obtener detalles de un usuario"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        if user_type == 'acudiente':
            user = get_object_or_404(Acudiente, id=user_id)
            
            # Calcular total de jugadores asociados
            total_jugadores = user.jugadores.count()
            jugadores_list = []
            for jugador in user.jugadores.all():
                jugadores_list.append({
                    'id': jugador.id,
                    'nombre': f"{jugador.nombre} {jugador.apellido}",
                    'identificacion': jugador.identificacion,
                    'edad': (date.today() - jugador.fecha_nacimiento).days // 365
                })
            
            data = {
                'tipo': 'Acudiente',
                'id': user.id,
                'nombre_completo': f"{user.nombre} {user.apellidos}",
                'tipo_documento': user.get_tipo_doc_display(),
                'identificacion': user.identificacion,
                'ciudad': user.ciudad,
                'direccion': user.direccion,
                'telefono': user.telefono,
                'correo': user.correo,
                'tipo_regimen': user.get_tipo_regimen_display(),
                'total_jugadores': total_jugadores,
                'jugadores': jugadores_list
            }
            
        elif user_type == 'jugador':
            user = get_object_or_404(Jugador, id=user_id)
            edad = (date.today() - user.fecha_nacimiento).days // 365
            
            data = {
                'tipo': 'Jugador',
                'id': user.id,
                'nombre_completo': f"{user.nombre} {user.apellido}",
                'tipo_documento': user.get_tipo_doc_display(),
                'identificacion': user.identificacion,
                'edad': edad,
                'fecha_nacimiento': user.fecha_nacimiento.strftime('%d/%m/%Y'),
                'ciudad': user.ciudad,
                'ciudad_nacimiento': user.ciudad_nacimiento,
                'direccion': user.direccion,
                'institucion_educativa': user.institucion_educativa,
                'jornada_entreno': user.get_jornada_entreno_display(),
                'tiene_enfermedad': 'Sí' if user.tiene_enfermedad else 'No',
                'tipo_enfermedad': user.tipo_enfermedad if user.tipo_enfermedad else 'N/A',
                'tiene_contraindicacion': 'Sí' if user.tiene_contraindicacion else 'No',
                'contacto_emergencia': user.contacto_emergencia,
                'num_contacto': user.num_contacto,
                'eps': user.eps,
                'parentesco': user.parentesco,
                'centro_atencion': user.centro_atencion,
                'acudiente': {
                    'id': user.acudiente.id,
                    'nombre': f"{user.acudiente.nombre} {user.acudiente.apellidos}",
                    'identificacion': user.acudiente.identificacion,
                    'telefono': user.acudiente.telefono,
                    'correo': user.acudiente.correo
                }
            }
            
        else:
            return JsonResponse({'error': 'Tipo de usuario no válido'}, status=400)
            
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ... otras funciones
@require_http_methods(["GET"])
def get_user_edit_form(request, user_type, pk):
    """
    Devuelve el HTML del formulario de edición (partial) ya ligado a la instancia.
    El frontend inyecta este HTML dentro del modal.
    """
    if user_type == 'acudiente':
        obj = get_object_or_404(Acudiente, pk=pk)
        form = AcudienteForm(instance=obj, editable=True)
        template = 'users/partials/acudiente_form.html'
    elif user_type == 'jugador':
        obj = get_object_or_404(Jugador, pk=pk)
        form = JugadorForm(instance=obj, editable=True)
        template = 'users/partials/jugador_form.html'
    else:
        return HttpResponseBadRequest('Tipo de usuario inválido.')

    html = render_to_string(template, {'form': form, 'obj': obj}, request=request)
    return HttpResponse(html)

@require_http_methods(["POST"])
def update_user(request, user_type, pk):
    """
    Recibe POST con los campos del formulario. Devuelve JSON {success: True} o errores.
    Es la vista que llamará tu JS cuando el usuario haga "Guardar".
    """
    if user_type == 'acudiente':
        obj = get_object_or_404(Acudiente, pk=pk)
        form = AcudienteForm(request.POST, instance=obj)
    elif user_type == 'jugador':
        obj = get_object_or_404(Jugador, pk=pk)
        form = JugadorForm(request.POST, instance=obj)
    else:
        return JsonResponse({'success': False, 'error': 'Tipo inválido.'}, status=400)

    if form.is_valid():
        form.save()
        return JsonResponse({'success': True, 'message': 'Usuario actualizado correctamente.'})
    else:
        # Devolvemos errores del formulario para mostrarlos en el modal
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)