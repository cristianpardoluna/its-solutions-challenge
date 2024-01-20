from functools import wraps
from django.http import HttpResponseForbidden, HttpResponse

from backend.models import Officer

def validate_officer_token(view):
    """ Esta función retorna un wrapper que
        envuelve una función de una vista para
        validar si en el header 'Authorization' de la solicitud
        existe una token asociada a un oficial.
        Si no es así retorna 403 Forbidden.
    """
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return HttpResponseForbidden("Una Bearer token es requerida")

        _, token = auth_header.split(" ", 1)
        try:
            officer = Officer.objects.get(token=token)
        except Officer.DoesNotExist:
            return HttpResponseForbidden("No se encuentra un oficial " +
            "asociado a esta token")

        request.officer = officer
        return view(request, *args, **kwargs)

    return wrapper