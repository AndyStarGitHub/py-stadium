from datetime import datetime

from django.utils.dateparse import parse_datetime
from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet

from stadium.models import (
    Actor,
    Event,
    EventSession,
    Genre,
    Order,
    Section,
    SportArena,
    Team,
)
from stadium.permissions import IsAdminOrIfAuthenticatedReadOnly
from stadium.serializers import (
    ActorSerializer,
    EventSerializer,
    EventListSerializer,
    EventRetrieveSerializer,
    EventSessionSerializer,
    EventSessionListSerializer,
    GenreSerializer,
    OrderSerializer,
    OrderListSerializer,
    SectionSerializer,
    SectionListSerializer,
    SectionRetrieveSerializer,
    SportArenaSerializer,
    SportArenaListSerializer,
    SportArenaRetrieveSerializer,
    TeamSerializer,
    EventSessionRetrieveSerializer,
)


class ActorViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    @staticmethod
    def _params_to_ints(qs):
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        queryset = self.queryset

        actors = self.request.query_params.get("actors")
        if actors:
            queryset = queryset.filter(actors__last_name__icontains=actors)

        genres = self.request.query_params.get("genres")
        if genres:
            queryset = queryset.filter(genres__name__icontains=genres)

        teams = self.request.query_params.get("teams")
        if teams:
            queryset = queryset.filter(teams__name__icontains=teams)

        if self.action in ("list", "retrieve"):
            return queryset.prefetch_related("genres")
        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return EventListSerializer
        elif self.action == "retrieve":
            return EventRetrieveSerializer
        return EventSerializer


# class EventViewSet(
#     mixins.CreateModelMixin,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     GenericViewSet,
# ):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
#     permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


# class EventSessionViewSet(
#     mixins.CreateModelMixin,
#     mixins.ListModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     GenericViewSet,
# ):
#     queryset = EventSession.objects.all()
#     serializer_class = EventSessionSerializer
#     permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

class EventSessionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    queryset = EventSession.objects.all()

    def get_queryset(self):
        queryset = self.queryset

        event = self.request.query_params.get("event")
        if event:
            queryset = queryset.filter(event__title__icontains=event)

        sportarena = self.request.query_params.get("sportarena")
        if sportarena:
            queryset = queryset.filter(sportarena__name__icontains=sportarena)

        show_time = self.request.query_params.get("show_time")
        if show_time:
            try:
                date_obj = datetime.strptime(show_time, "%Y-%m-%d").date()
                queryset = queryset.filter(show_time__date=date_obj)
            except ValueError:
                pass

        if self.action in ("list", "retrieve"):
            return queryset.select_related("event")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return EventSessionListSerializer
        if self.action == "retrieve":
            return EventSessionRetrieveSerializer

        return EventSessionSerializer



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
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class SectionViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Section.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list':
            return SectionListSerializer
        elif self.action == 'retrieve':
            return SectionRetrieveSerializer
        return SectionSerializer


class SportArenaViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = SportArena.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == 'list':
            return SportArenaListSerializer
        elif self.action == 'retrieve':
            return SportArenaRetrieveSerializer
        return SportArenaSerializer


class TeamViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)



class OrderSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 20


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderSetPagination
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        if self.action in ("list", "retrieve"):
            queryset = queryset.prefetch_related("ticket_orders")
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == 'list':
            serializer = OrderListSerializer
        return serializer
