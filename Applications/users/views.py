from django.shortcuts import render
from django.http import HttpResponse
from .models import Acudiente, Jugador

# Create your views here.

def usersManagement(request):
    acudientes = Acudiente.objects.all()
    return render(request, "index.html", {
        "acudientes": acudientes,
        "acudientes_count": acudientes.count(),
    })