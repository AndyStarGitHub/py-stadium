from django.contrib import admin

from django.contrib import admin

from .models import (
    SportArena,
    Section,
    Genre,
    Actor,
    Event,
    EventSession,
    Order,
    Ticket,
    Team,
)

admin.site.register(SportArena)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Section)
admin.site.register(Event)
admin.site.register(EventSession)
admin.site.register(Order)
admin.site.register(Team)
admin.site.register(Ticket)

