from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from datetime import date, timedelta
from .models import Acudiente, Jugador

# Create your views here.

def usersManagement(request):
    # Obtener parámetros de filtro
    search = request.GET.get('search', '')
    tipo_doc = request.GET.get('tipo_doc', '')
    ciudad = request.GET.get('ciudad', '')
    tipo_usuario = request.GET.get('tipo_usuario', '')
    
    # Filtrar acudientes
    acudientes = Acudiente.objects.all()
    
    #Filtro de Busqueda General
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
    
    
    
    context = {
        'acudientes': acudientes,
        'jugadores': jugadores,
        'ciudades_disponibles': ciudades_disponibles,
    }
    return render(request, 'index.html', context)

def busqueda_avanzada(request):
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
    regimen = request.GET.get('regimen', '')
    
    # Filtrar acudientes
    acudientes = Acudiente.objects.all()
    
    if search:
        acudientes = acudientes.filter(
            Q(nombre__icontains=search) |
            Q(apellidos__icontains=search) |
            Q(identificacion__icontains=search) |
            Q(correo__icontains=search)
        )
    
    if tipo_doc:
        acudientes = acudientes.filter(tipo_doc=tipo_doc)
    
    if ciudad:
        acudientes = acudientes.filter(ciudad=ciudad)
        
    if correo:
        acudientes = acudientes.filter(correo__icontains=correo)
        
    if regimen:
        acudientes = acudientes.filter(tipo_regimen=regimen)
    
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
        'total_resultados': total_resultados,
    }
    return render(request, 'busqueda_avanzada.html', context)