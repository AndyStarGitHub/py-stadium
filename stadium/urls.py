from django.urls import path, include
from rest_framework import routers

from stadium.views import (
    ActorViewSet,
    GenreViewSet,
    SportArenaViewSet,
    SectionViewSet
)

router = routers.DefaultRouter()
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("sections", SectionViewSet)
router.register("sport_arenas", SportArenaViewSet)
# router.register("actors", ActorViewSet)
# router.register("cinema_halls", CinemaHallViewSet)
# router.register("movies", MovieViewSet)
# router.register("movie_sessions", MovieSessionViewSet)
# router.register("orders", OrderViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "stadium"