from django.shortcuts import render
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import GenericViewSet

from stadium.models import Genre, SportArena
from stadium.permissions import IsAdminOrIfAuthenticatedReadOnly
from stadium.serializers import GenreSerializer, SportArenaSerializer


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class SportArenaViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = SportArena.objects.all()
    serializer_class = SportArenaSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
