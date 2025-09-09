# Logic behind users templates (real function)
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from datetime import date, timedelta
from .models import Guardian, Player
from .forms import  GuardianForm, PlayerForm
from django.template.loader import render_to_string

# Create your views here.
# Requirement FR-06

def create_player(request):
    form = PlayerForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return render(request, 'create_player.html', {'form': PlayerForm(), 'success': True})
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors, 'form_html': form.as_p()})
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return HttpResponse(form.as_p())
    return render(request, 'create_player.html', {'form': form})

# Requirement FR-21
def create_guardian(request):
    form = GuardianForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return render(request, 'create_guardian.html', {'form': GuardianForm(), 'success': True})
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
    players = Player.objects.select_related('fk_guardian').all()

    if search:
        search_words = search.strip().split()
        if len(search_words) > 1:
            player_query = Q()
            for word in search_words:
                player_query &= (
                    Q(first_name__icontains=word) |
                    Q(last_name__icontains=word) |
                    Q(identification__icontains=word) |
                    Q(fk_guardian__first_name__icontains=word) |
                    Q(fk_guardian__last_name__icontains=word) |
                    Q(educational_institution__icontains=word)
                )
            players = players.filter(player_query)
        else:
            players = players.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(identification__icontains=search) |
                Q(fk_guardian__first_name__icontains=search) |
                Q(fk_guardian__last_name__icontains=search) |
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
    return render(request, 'user_management.html', context)

def display_user_advanced(request): # Advanced search view

    # View for advanced search with multiple filters
    # The 'variable' comes from the HTML, the input obtained from the GET request.

    # Basic parameters
    search = request.GET.get('search', '').strip()
    user_type = request.GET.get('user_type', '').strip()
    city = request.GET.get('city', '').strip()
    document_type = request.GET.get('document_type', '').strip()

    # Player-specific parameters
    educational_institution = request.GET.get('educational_institution', '').strip()
    training_session = request.GET.get('training_session', '').strip()
    age_range = request.GET.get('age_range', '').strip()
    has_disease = request.GET.get('has_disease', '').strip()

    # Guardian-specific parameters
    email = request.GET.get('email', '').strip()
    regime_type = request.GET.get('regime_type', '').strip()  # Updated to English for consistency

    # Detect if player-specific filters are being used (after strip, empty strings are falsy)
    player_filters_used = any([educational_institution, training_session, age_range, has_disease])
    
    # Detect if guardian-specific filters are being used (after strip, empty strings are falsy)
    guardian_filters_used = any([email, regime_type])
    
    # Auto-determine user type based on specific filters
    if player_filters_used and not guardian_filters_used and not user_type:
        user_type = 'players'
    elif guardian_filters_used and not player_filters_used and not user_type:
        user_type = 'guardians'

    # Filter guardians
    guardians = Guardian.objects.all()
    if search:
        search_words = search.split()
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
    
    # Obtener valores únicos de tipo_regimen en la base (Acudientes)
    regime_types_in_db = list(Guardian.objects.values_list('regime_type', flat=True).distinct())
    
    # Crear mapa para ordenar según orden_regimen
    index_map_regime = {label: idx for idx, label in enumerate(regime_order)}
    
    # Ordenar los valores obtenidos de la BD según el orden definido
    regime_types_in_db.sort(key=lambda x: index_map_regime.get(x, len(index_map_regime)))

    # If only players are wanted, empty guardians
    if user_type == 'players':
        guardians = Guardian.objects.none()

    # Filter players
    players = Player.objects.select_related('fk_guardian').all()
    
    if search:
        # Dividir la búsqueda en palabras para permitir buscar nombre y apellido por separado
        search_words = search.split()
        
        if len(search_words) > 1:
             # Si hay múltiples palabras, buscar que contengan todas las palabras
            player_query = Q()
            for word in search_words:
                player_query &= (
                    Q(first_name__icontains=word) |
                    Q(last_name__icontains=word) |
                    Q(identification__icontains=word) |
                    Q(fk_guardian__first_name__icontains=word) |
                    Q(fk_guardian__last_name__icontains=word) |
                    Q(educational_institution__icontains=word)
                )
            players = players.filter(player_query)
        else:
            # Si es una sola palabra, usar el comportamiento original
            players = players.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(identification__icontains=search) |
                Q(fk_guardian__first_name__icontains=search) |
                Q(fk_guardian__last_name__icontains=search) |
                Q(educational_institution__icontains=search)
            )
    
    if document_type:
        players = players.filter(document_type=document_type)
    
    if city:
        players = players.filter(city=city)
    
    if educational_institution:
        players = players.filter(educational_institution__icontains=educational_institution)

    if training_session:
        players = players.filter(training_session=training_session)

    if has_disease:
        players = players.filter(has_disease=(has_disease == 'true'))

    # Filtro por rango de edad
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
        else:
            start_date, end_date = None, None
        if start_date and end_date:
            players = players.filter(birth_date__range=[start_date, end_date])
    
    # If only guardians are wanted, empty players
    if user_type == 'guardians':
        players = Player.objects.none()
    
    # Add calculated age to players (more efficient than loop)
    if players.exists():
        for player in players:
            player.age = (date.today() - player.birth_date).days // 365
    
    # Get available cities (optimize queries)
    guardian_cities = set(Guardian.objects.values_list('city', flat=True).distinct())
    player_cities = set(Player.objects.values_list('city', flat=True).distinct())
    available_cities = sorted(guardian_cities.union(player_cities))
    
    # Document type order (optimize with better sorting)
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
    
    return render(request, 'user_management_advanced.html', context)

def get_user_details(request, user_type, user_id): #'Ver' Button logic
    
    # Vista AJAX para obtener detalles de un usuario
    if request.method != 'GET':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    try:
        if user_type == 'guardian':
            user = get_object_or_404(Guardian, id=user_id)

            # Calcular total de jugadores asociados
            total_players = user.players.count()
            players_list = []
            for player in user.players.all():
                players_list.append({
                    'id': player.id,
                    'name': f"{player.first_name} {player.last_name}",
                    'identification': player.identification,
                    'age': (date.today() - player.birth_date).days // 365
                })
            
            data = {
                'type': 'Guardian',
                'id': user.id,
                'name': f"{user.first_name} {user.last_name}",
                'document_type': user.get_document_type_display(),
                'identification': user.identification,
                'city': user.city,
                'address': user.address,
                'phone': user.phone,
                'email': user.email,
                'regime_type': user.get_regime_type_display(),
                'total_players': total_players,
                'players': players_list
            }
            
        elif user_type == 'player':
            user = get_object_or_404(Player, id=user_id)
            age = (date.today() - user.birth_date).days // 365

            data = {
                'type': 'Player',
                'id': user.id,
                'name': f"{user.first_name} {user.last_name}",
                'document_type': user.get_document_type_display(),
                'identification': user.identification,
                'age': age,
                'birth_date': user.birth_date.strftime('%d/%m/%Y'),
                'city': user.city,
                'birth_city': user.birth_city,
                'address': user.address,
                'educational_institution': user.educational_institution,  # Corregido para coincidir con el modelo
                'training_session': user.get_training_session_display(),
                'has_disease': 'Sí' if user.has_disease else 'No',
                'disease_type': user.disease_type if user.disease_type else 'N/A',
                'has_contraindication': 'Sí' if user.has_contraindication else 'No',
                'emergency_contact': user.emergency_contact,
                'emergency_contact_number': user.contact_number,  # Corregido para coincidir con el modelo
                'health_center': user.health_center,
                'kinship': user.kinship,
                'eps': user.eps,
                'fk_guardian': {
                    'id': user.fk_guardian.id,
                    'name': f"{user.fk_guardian.first_name} {user.fk_guardian.last_name}",
                    'identification': user.fk_guardian.identification,
                    'phone': user.fk_guardian.phone,
                    'email': user.fk_guardian.email
                }
            }
            
        else:
            return JsonResponse({'error': 'Tipo de usuario no válido'}, status=400)
            
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_user_edit_form(request, user_type, user_id):
    try:
        if user_type == 'guardian':
            user = get_object_or_404(Guardian, id=user_id)
            form = GuardianForm(instance=user, editable=True)
        elif user_type == 'player':
            user = get_object_or_404(Player, id=user_id)
            form = PlayerForm(instance=user, editable=True)
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
        if user_type == 'guardian':
            user = get_object_or_404(Guardian, id=user_id)
            form = GuardianForm(request.POST, instance=user, editable=True)
        elif user_type == 'player':
            user = get_object_or_404(Player, id=user_id)
            form = PlayerForm(request.POST, instance=user, editable=True)
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
        if user_type == 'guardian':
            user = get_object_or_404(Guardian, id=user_id)
            # Verificar si tiene jugadores asociados antes de eliminar
            if user.players.exists():
                return JsonResponse({
                    'error': 'No se puede eliminar este guardián porque tiene jugadores asociados. '
                             'Primero debe reassignar o eliminar los jugadores.'
                }, status=400)
        elif user_type == 'player':
            user = get_object_or_404(Player, id=user_id)
        else:
            return JsonResponse({'error': 'Tipo de usuario no válido'}, status=400)

        user.delete()
        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)