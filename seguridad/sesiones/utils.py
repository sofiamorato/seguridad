# sesiones/utils.py

from .models import Session

def check_multiple_sessions(user_id):
    """
    Verifica si un usuario tiene más de una sesión activa.
    """
    active_sessions = Session.objects.filter(user_id=user_id, active=True)
    return active_sessions.count() > 1
