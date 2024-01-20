from django.contrib import admin
from backend.models import Person, Vehicle, Officer, Infraction

admin.site.register(Person)
admin.site.register(Vehicle)
admin.site.register(Officer)
admin.site.register(Infraction)