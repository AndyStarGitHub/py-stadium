from django.contrib import admin

from .models import (
    Genre,
    Actor,
    Event,
    EventSession,
    Team,
)

admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Event)
admin.site.register(EventSession)
admin.site.register(Team)
