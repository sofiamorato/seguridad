# sesiones/views.py

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Session
from .utils import check_multiple_sessions
import datetime

@login_required
def create_session(request):
    ip = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT')

    # Registrar una nueva sesión activa
    session = Session.objects.create(
        user=request.user,
        ip=ip,
        user_agent=user_agent,
        login_time=datetime.datetime.now(),
        last_activity=datetime.datetime.now(),
        active=True
    )
    session.save()

    return HttpResponse(f"Sesión registrada para el usuario {request.user.username}")

@login_required
def check_sessions(request):
    if check_multiple_sessions(request.user.id):
        return HttpResponse("Alerta: El usuario tiene múltiples sesiones activas.")
    return HttpResponse("El usuario tiene solo una sesión activa.")
