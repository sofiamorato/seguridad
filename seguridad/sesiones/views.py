from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Session

def home(request):
    """
    Página principal: muestra formularios de registro e inicio de sesión.
    Cuando el usuario inicia sesión, se crea una entrada en Session y,
    si hay más de una activa, se muestra la alerta en la misma página.
    """
    register_form = UserCreationForm()
    login_form = AuthenticationForm()
    message = None
    sessions_count = 0

    # Registro
    if request.method == 'POST' and 'register' in request.POST:
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            message = f"Usuario '{user.username}' creado correctamente. Ahora inicia sesión."

    # Login
    elif request.method == 'POST' and 'login' in request.POST:
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            auth_login(request, user)

            # Crear registro de sesión
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

            # Contar sesiones activas
            sessions_count = Session.objects.filter(user=user, active=True).count()
            if sessions_count > 1:
                message = f"⚠️ Alerta: el usuario {user.username} tiene {sessions_count} sesiones activas."
            else:
                message = f"✅ Sesión iniciada correctamente para {user.username}."

    return render(request, 'sesiones/home.html', {
        'register_form': register_form,
        'login_form': login_form,
        'message': message,
        'sessions_count': sessions_count,
    })


@login_required
def logout_view(request):
    """Cierra la sesión Django y marca todas las sesiones del usuario como inactivas."""
    Session.objects.filter(user=request.user, active=True).update(active=False)
    auth_logout(request)
    return redirect('home')
