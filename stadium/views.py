from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from stadium.models import Genre
from stadium.permissions import IsAdminOrIfAuthenticatedReadOnly
from stadium.serializers import GenreSerializer


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
