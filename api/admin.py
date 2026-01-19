from django.contrib import admin

from .models import Event, Photographer, Assignment

admin.site.register(Event)
admin.site.register(Photographer)
admin.site.register(Assignment)
