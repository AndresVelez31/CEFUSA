# Logic behind users templates (real function)
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from datetime import date, timedelta
from .models import Attendant, Player
from .forms import AcudienteForm, JugadorForm
from django.template.loader import render_to_string

# Create your views here.
# Requirement FR-06

def create_player(request):
    form = JugadorForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return render(request, 'createJugador.html', {'form': JugadorForm(), 'success': True})
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors, 'form_html': form.as_p()})
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return HttpResponse(form.as_p())
    return render(request, 'create_player.html', {'form': form})

# Requirement FR-21
def create_guardian(request):
    form = AcudienteForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return render(request, 'createAcudiente.html', {'form': AcudienteForm(), 'success': True})
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors, 'form_html': form.as_p()})
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return HttpResponse(form.as_p())
    return render(request, 'create_guardian.html', {'form': form})

def display_user(request): # Basic research
    # Get filter parameters
    search = request.GET.get('search', '')
    doc_type = request.GET.get('tipo_doc', '')
    city = request.GET.get('ciudad', '')
    user_type = request.GET.get('tipo_usuario', '')

    # Filter attendants
    attendants = Attendant.objects.all()

    # General search filter
    if search:
        search_words = search.strip().split()
        if len(search_words) > 1:
            attendant_query = Q()
            for word in search_words:
                attendant_query &= (
                    Q(first_name__icontains=word) |
                    Q(last_name__icontains=word) |
                    Q(identification__icontains=word) |
                    Q(email__icontains=word) |
                    Q(city__icontains=word) |
                    Q(phone__icontains=word) |
                    Q(address__icontains=word) |
                    Q(regime_type__icontains=word) |
                    Q(document_type__icontains=word)
                )
            attendants = attendants.filter(attendant_query)
        else:
            attendants = attendants.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(identification__icontains=search) |
                Q(email__icontains=search) |
                Q(city__icontains=search) |
                Q(phone__icontains=search) |
                Q(address__icontains=search) |
                Q(regime_type__icontains=search) |
                Q(document_type__icontains=search)
            )

    # Document type filter
    if doc_type:
        attendants = attendants.filter(document_type=doc_type)

    # City filter
    if city:
        attendants = attendants.filter(city=city)

    # If only players are wanted, empty attendants
    if user_type == 'jugadores':
        attendants = Attendant.objects.none()

    # Filter players
    players = Player.objects.select_related('attendant').all()

    if search:
        search_words = search.strip().split()
        if len(search_words) > 1:
            player_query = Q()
            for word in search_words:
                player_query &= (
                    Q(first_name__icontains=word) |
                    Q(last_name__icontains=word) |
                    Q(identification__icontains=word) |
                    Q(attendant__first_name__icontains=word) |
                    Q(attendant__last_name__icontains=word) |
                    Q(educational_institution__icontains=word)
                )
            players = players.filter(player_query)
        else:
            players = players.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(identification__icontains=search) |
                Q(attendant__first_name__icontains=search) |
                Q(attendant__last_name__icontains=search) |
                Q(educational_institution__icontains=search)
            )

    if doc_type:
        players = players.filter(document_type=doc_type)

    if city:
        players = players.filter(city=city)

    # If only attendants are wanted, empty players
    if user_type == 'acudientes':
        players = Player.objects.none()

    # Get available cities for filter
    attendant_cities = set(Attendant.objects.values_list('city', flat=True).distinct())
    player_cities = set(Player.objects.values_list('city', flat=True).distinct())
    available_cities = sorted(attendant_cities.union(player_cities))

    # Order to use (from TextChoices)
    doc_type_order = [option.label for option in Attendant.DocumentType]

    # Get document types from both models
    attendant_doc_types = set(Attendant.objects.values_list('document_type', flat=True).distinct())
    player_doc_types = set(Player.objects.values_list('document_type', flat=True).distinct())

    # Merge types and convert to list
    doc_types_in_db = list(attendant_doc_types.union(player_doc_types))

    # Create index map for custom order
    index_map = {label: idx for idx, label in enumerate(doc_type_order)}

    # Sort according to defined order, unknowns at the end
    doc_types_in_db.sort(key=lambda x: index_map.get(x, len(index_map)))

    context = {
        'attendants': attendants,
        'players': players,
        'available_cities': available_cities,
        'doc_types_in_db': doc_types_in_db
    }
    return render(request, 'index.html', context)

def display_user_advanced(request): # Advanced search view

    # Vista para búsqueda avanzada con filtros específicos

    # Parámetros básicos
    search = request.GET.get('search', '')
    tipo_usuario = request.GET.get('tipo_usuario', '')
    ciudad = request.GET.get('ciudad', '')
    tipo_doc = request.GET.get('tipo_doc', '')
    
    # Parámetros específicos de jugadores
    institucion = request.GET.get('institucion', '')
    jornada = request.GET.get('jornada', '')
    rango_edad = request.GET.get('rango_edad', '')
    
    # Parámetros específicos de acudientes
    correo = request.GET.get('correo', '')
    tipo_regimen = request.GET.get('tipo_regimen', '')

    # Filtrar acudientes
    acudientes = Acudiente.objects.all()
    if search:
        # Dividir la búsqueda en palabras para permitir buscar nombre y apellido por separado
        search_words = search.strip().split()
        if len(search_words) > 1:
            # Si hay múltiples palabras, buscar que contengan todas las palabras
            acudiente_query = Q()
            for word in search_words:
                acudiente_query &= (
                    Q(nombre__icontains=word) |
                    Q(apellidos__icontains=word) |
                    Q(identificacion__icontains=word) |
                    Q(correo__icontains=word) |
                    Q(ciudad__icontains=word) |
                    Q(telefono__icontains=word) |
                    Q(direccion__icontains=word) |
                    Q(tipo_regimen__icontains=word) |
                    Q(tipo_doc__icontains=word)
                )
            acudientes = acudientes.filter(acudiente_query)
        else:
            # Si es una sola palabra, usar el comportamiento original
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
        # Dividir la búsqueda en palabras para permitir buscar nombre y apellido por separado
        search_words = search.strip().split()
        
        if len(search_words) > 1:
            # Si hay múltiples palabras, buscar que contengan todas las palabras
            jugador_query = Q()
            for word in search_words:
                jugador_query &= (
                    Q(nombre__icontains=word) |
                    Q(apellido__icontains=word) |
                    Q(identificacion__icontains=word) |
                    Q(acudiente__nombre__icontains=word) |
                    Q(acudiente__apellidos__icontains=word) |
                    Q(institucion_educativa__icontains=word)
                )
            jugadores = jugadores.filter(jugador_query)
        else:
            # Si es una sola palabra, usar el comportamiento original
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
    return render(request, 'advanced_search.html', context)

def get_user_details(request, user_type, user_id): #'Ver' Button logic
    # Vista AJAX para obtener detalles de un usuario
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

def get_user_edit_form(request, user_type, user_id):
    try:
        if user_type == 'acudiente':
            user = get_object_or_404(Acudiente, id=user_id)
            form = AcudienteForm(instance=user, editable=True)
        elif user_type == 'jugador':
            user = get_object_or_404(Jugador, id=user_id)
            form = JugadorForm(instance=user, editable=True)
        else:
            return JsonResponse({'error': 'Tipo de usuario no válido'}, status=400)
        html_content = render_to_string(
            'get_user_edit_form.html', 
            {'form': form},
            request=request
        )
        return HttpResponse(html_content)
    except Exception as e:
        # Si hay error, mostrar mensaje claro en el formulario
        error_html = f'<div class="alert alert-danger">Error al cargar el formulario: {str(e)}</div>'
        return HttpResponse(error_html)

def update_user(request, user_type, user_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        if user_type == 'acudiente':
            user = get_object_or_404(Acudiente, id=user_id)
            form = AcudienteForm(request.POST, instance=user, editable=True)
        elif user_type == 'jugador':
            user = get_object_or_404(Jugador, id=user_id)
            form = JugadorForm(request.POST, instance=user, editable=True)
        else:
            return JsonResponse({'error': 'Tipo de usuario no válido'}, status=400)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def delete_user(request, user_type, user_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        if user_type == 'acudiente':
            user = get_object_or_404(Acudiente, id=user_id)
            # Verificar si tiene jugadores asociados antes de eliminar
            if user.jugadores.exists():
                return JsonResponse({
                    'error': 'No se puede eliminar este acudiente porque tiene jugadores asociados. '
                             'Primero debe reassignar o eliminar los jugadores.'
                }, status=400)
        elif user_type == 'jugador':
            user = get_object_or_404(Jugador, id=user_id)
        else:
            return JsonResponse({'error': 'Tipo de usuario no válido'}, status=400)

        user.delete()
        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)