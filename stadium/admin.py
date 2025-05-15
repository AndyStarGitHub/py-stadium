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


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInline,)


admin.site.register(SportArena)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Section)
admin.site.register(Event)
admin.site.register(EventSession)
# admin.site.register(Order, OrderAdmin)
admin.site.register(Team)
admin.site.register(Ticket)
