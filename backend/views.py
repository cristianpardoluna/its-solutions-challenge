import json

from django.http import request, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from backend.models import Infraction, Officer, Vehicle, Person
from backend.wrapper import validate_officer_token

@csrf_exempt
@require_http_methods(["POST"])
@validate_officer_token
def cargar_infraccion(request):
    """ Vista que permite a un oficial subir una infracción asociada
        a un vehículo existente.
        El método de autenticación se encuentra en el wrapper
        validate_officer_token y está basado en token.
    """
    response = HttpResponse()
    # Recibir el cuerpo de la solicitud como una cadena tipo JSON
    body = json.loads(request.body.decode("utf-8"))
    plate = body.get("placa_patente")
    comments = body.get("comentarios")

    # Validar si la placa está asociada a un vehículo
    try:
        vehicle = Vehicle.objects.get(plate=plate)
    except Vehicle.DoesNotExist:
        response.status_code = 404
        response.content = "No existe un vehículo asociado a la placa"
        return response

    new_infraction = Infraction(
        vehicle=vehicle,
        comments=comments,
        officer=request.officer
    )
    new_infraction.save()
    response.content = new_infraction.pk
    return response

@require_http_methods(["GET"])
def generar_informe(request):
    """ Vista para retornar un informe en formato JSON
        de las infracciones asociadas al vehículo(s) de las persona
        asociada al email pasado en el parámetro de query 'email'
    """
    response = HttpResponse()
    email = request.GET.get("email")
    try:
        Person.objects.get(email=email)
    except Person.DoesNotExist:
        response.status_code = 404
        response.content = "El email no se encuentra asociado " + \
            "ninguna persona"
        return response

    infractions = Infraction.objects.filter(vehicle__owner__email=email)\
        .values()
    return JsonResponse(list(infractions), safe=False)