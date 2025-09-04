# Logic behind users templates (real function)
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from datetime import date, timedelta
from .models import Guardian, Player
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

    #The 'variable' comes from the HTML, the input obtained from the GET request.

    search = request.GET.get('search', '')
    document_type = request.GET.get('document_type', '')  # Cambiado a 'document_type' para uniformidad con models
    city = request.GET.get('city', '')  # Mantener 'ciudad' porque es el nombre esperado en la URL
    user_type = request.GET.get('user_type', '')  # Mantener 'tipo_usuario' porque es el nombre esperado en la URL

    # Filter guardians
    guardians = Guardian.objects.all()

    # General search filter
    if search:
        search_words = search.strip().split()
        if len(search_words) > 1:
            guardian_query = Q()
            for word in search_words:
                guardian_query &= (
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
            guardians = guardians.filter(guardian_query)
        else:
            guardians = guardians.filter(
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
    #In the comparison the left one is from the models, the right one from the GET parameter/HTML
    if document_type:
        guardians = guardians.filter(document_type=document_type)

    # City filter
    if city:
        guardians = guardians.filter(city=city)

    # If only players are wanted, empty guardians
    if user_type == 'players':
        guardians = Guardian.objects.none()

    # Filter players
    players = Player.objects.select_related('guardian').all()

    if search:
        search_words = search.strip().split()
        if len(search_words) > 1:
            player_query = Q()
            for word in search_words:
                player_query &= (
                    Q(first_name__icontains=word) |
                    Q(last_name__icontains=word) |
                    Q(identification__icontains=word) |
                    Q(guardian__first_name__icontains=word) |
                    Q(guardian__last_name__icontains=word) |
                    Q(educational_institution__icontains=word)
                )
            players = players.filter(player_query)
        else:
            players = players.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(identification__icontains=search) |
                Q(guardian__first_name__icontains=search) |
                Q(guardian__last_name__icontains=search) |
                Q(educational_institution__icontains=search)
            )

    if document_type:
        players = players.filter(document_type=document_type)

    if city:
        players = players.filter(city=city)

    # If only guardians are wanted, empty players
    if user_type == 'guardians':
        players = Player.objects.none()

    # Get available cities for filter
    guardian_cities = set(Guardian.objects.values_list('city', flat=True).distinct())
    player_cities = set(Player.objects.values_list('city', flat=True).distinct())
    available_cities = sorted(guardian_cities.union(player_cities))

    # Order to use (from TextChoices)
    document_type_order = [option.label for option in Guardian.DocumentType]

    # Get document types from both models
    guardian_document_types = set(Guardian.objects.values_list('document_type', flat=True).distinct())
    player_document_types = set(Player.objects.values_list('document_type', flat=True).distinct())

    # Merge types and convert to list
    document_types_in_db = list(guardian_document_types.union(player_document_types))

    # Create index map for custom order
    index_map = {label: idx for idx, label in enumerate(document_type_order)}

    # Sort according to defined order, unknowns at the end
    document_types_in_db.sort(key=lambda x: index_map.get(x, len(index_map)))

    context = {
        'guardians': guardians,  # Mantener en inglés porque es código
        'players': players,  # Mantener en inglés porque es código
        'available_cities': available_cities,  # Mantener en inglés porque es código
        'document_types_in_db': document_types_in_db  # Cambiado a 'document_types_in_db' para uniformidad
    }
    return render(request, 'index.html', context)

def display_user_advanced(request): # Advanced search view

    # View for advanced search with multiple filters

    # Basic parameters
    search = request.GET.get('search', '')
    user_type = request.GET.get('tipo_usuario', '')
    city = request.GET.get('ciudad', '')
    document_type = request.GET.get('tipo_doc', '')
    
    # Player-specific parameters
    institution = request.GET.get('institucion', '')
    session = request.GET.get('jornada', '')
    age_range = request.GET.get('rango_edad', '')
    
    # Guardian-specific parameters
    email = request.GET.get('correo', '')
    regime_type = request.GET.get('tipo_regimen', '')

    # Filter guardians
    guardians = Guardian.objects.all()
    if search:
        search_words = search.strip().split()
        if len(search_words) > 1:
            guardian_query = Q()
            for word in search_words:
                guardian_query &= (
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
            guardians = guardians.filter(guardian_query)
        else:
            guardians = guardians.filter(
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
    if document_type:
        guardians = guardians.filter(document_type=document_type)
    
    if city:
        guardians = guardians.filter(city=city)
    
    if email:
        guardians = guardians.filter(email__icontains=email)
    
    if regime_type:
        guardians = guardians.filter(regime_type=regime_type)

    # Order from TextChoices
    regime_order = [option.label for option in Guardian.RegimeType]
    regime_types_in_db = list(Guardian.objects.values_list('regime_type', flat=True).distinct())
    index_map_regime = {label: idx for idx, label in enumerate(regime_order)}
    regime_types_in_db.sort(key=lambda x: index_map_regime.get(x, len(index_map_regime)))

    # If only players are wanted, empty guardians
    if user_type == 'jugadores':
        guardians = Guardian.objects.none()

    # Filter players
    players = Player.objects.select_related('guardian').all()
    if search:
        search_words = search.strip().split()
        if len(search_words) > 1:
            player_query = Q()
            for word in search_words:
                player_query &= (
                    Q(first_name__icontains=word) |
                    Q(last_name__icontains=word) |
                    Q(identification__icontains=word) |
                    Q(guardian__first_name__icontains=word) |
                    Q(guardian__last_name__icontains=word) |
                    Q(educational_institution__icontains=word)
                )
            players = players.filter(player_query)
        else:
            players = players.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(identification__icontains=search) |
                Q(guardian__first_name__icontains=search) |
                Q(guardian__last_name__icontains=search) |
                Q(educational_institution__icontains=search)
            )
    
    if document_type:
        players = players.filter(document_type=document_type)
    
    if city:
        players = players.filter(city=city)
    
    if institution:
        players = players.filter(educational_institution__icontains=institution)
    
    if session:
        players = players.filter(training_session=session)
    
    if age_range:
        today = date.today()
        if age_range == '5-10':
            start_date = today - timedelta(days=10*365)
            end_date = today - timedelta(days=5*365)
        elif age_range == '11-15':
            start_date = today - timedelta(days=15*365)
            end_date = today - timedelta(days=11*365)
        elif age_range == '16-20':
            start_date = today - timedelta(days=20*365)
            end_date = today - timedelta(days=16*365)
        players = players.filter(birth_date__range=[start_date, end_date])
    
    # If only guardians are wanted, empty players
    if user_type == 'acudientes':
        players = Player.objects.none()
    
    # Add calculated age to players
    for player in players:
        player.age = (date.today() - player.birth_date).days // 365
    
    # Get available cities
    guardian_cities = set(Guardian.objects.values_list('city', flat=True).distinct())
    player_cities = set(Player.objects.values_list('city', flat=True).distinct())
    available_cities = sorted(guardian_cities.union(player_cities))
    
    # Document type order
    document_type_order = [option.label for option in Guardian.DocumentType]
    guardian_document_types = set(Guardian.objects.values_list('document_type', flat=True).distinct())
    player_document_types = set(Player.objects.values_list('document_type', flat=True).distinct())
    document_types_in_db = list(guardian_document_types.union(player_document_types))
    index_map = {label: idx for idx, label in enumerate(document_type_order)}
    document_types_in_db.sort(key=lambda x: index_map.get(x, len(index_map)))
    total_results = guardians.count() + players.count()
    
    context = {
        'guardians': guardians,
        'players': players,
        'available_cities': available_cities,
        'document_types_in_db': document_types_in_db,
        'regime_types_in_db': regime_types_in_db,
        'total_results': total_results
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