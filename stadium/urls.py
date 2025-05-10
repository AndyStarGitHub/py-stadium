from django.urls import path, include
from rest_framework import routers

from stadium.views import (
    ActorViewSet,
    EventViewSet,
    EventSessionViewSet,
    GenreViewSet,
    SectionViewSet,
    SportArenaViewSet,
    TeamViewSet,
)

router = routers.DefaultRouter()
router.register("actors", ActorViewSet)
router.register("events", EventViewSet)
router.register("eventsessions", EventSessionViewSet)
router.register("genres", GenreViewSet)
router.register("sections", SectionViewSet)
router.register("sport_arenas", SportArenaViewSet)
router.register("teams", TeamViewSet)

# router.register("cinema_halls", CinemaHallViewSet)
# router.register("movies", MovieViewSet)
# router.register("movie_sessions", MovieSessionViewSet)
# router.register("orders", OrderViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "stadium"