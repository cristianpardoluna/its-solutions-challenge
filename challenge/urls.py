from django.contrib import admin
from django.urls import path

from backend.views import cargar_infraccion, generar_informe

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cargar_infraccion/', cargar_infraccion),
    path('generar_informe/', generar_informe)
]
