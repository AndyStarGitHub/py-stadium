from django.contrib import admin

from .models import (
    SportArena,
    Section,
)

admin.site.register(SportArena)
admin.site.register(Section)
