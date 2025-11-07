# sesiones/middleware.py

import datetime
from .models import Session

class SessionUpdateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            # Actualizar la actividad de la sesión
            Session.objects.filter(user=request.user, active=True).update(last_activity=datetime.datetime.now())

        return response
