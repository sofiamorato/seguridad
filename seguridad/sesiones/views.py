from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Session

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Session

def home(request):
    register_form = UserCreationForm()
    login_form = AuthenticationForm()
    message = None
    sessions_count = 0

    # Registro de nuevo usuario
    if request.method == 'POST' and 'register' in request.POST:
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            message = f"Usuario '{user.username}' creado correctamente. Ahora inicia sesión."

    # Inicio de sesión
    elif request.method == 'POST' and 'login' in request.POST:
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()

            # Verificar cuántas sesiones activas tiene antes de permitir ingreso
            active_sessions = Session.objects.filter(user=user, active=True).count()
            if active_sessions >= 1:
               
                message = f" No se permite ingresar. El usuario '{user.username}' ya tiene {active_sessions} sesión activa."
            else:
                # Permitir el login
                auth_login(request, user)
                ip = request.META.get('REMOTE_ADDR')
                user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
                Session.objects.create(
                    user=user,
                    ip=ip,
                    user_agent=user_agent,
                    login_time=timezone.now(),
                    last_activity=timezone.now(),
                    active=True
                )
                message = f"Sesión iniciada correctamente para {user.username}."
                sessions_count = 1

    return render(request, 'sesiones/home.html', {
        'register_form': register_form,
        'login_form': login_form,
        'message': message,
        'sessions_count': sessions_count,
    })


@login_required
def logout_view(request):
    # Cierra la sesión y marca las sesiones activas como inactivas
    Session.objects.filter(user=request.user, active=True).update(active=False)
    auth_logout(request)
    return redirect('home')
