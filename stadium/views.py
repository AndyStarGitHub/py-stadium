from datetime import datetime

from drf_spectacular.utils import extend_schema, OpenApiParameter
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


class EventSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 20


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    pagination_class = EventSetPagination

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="actors",
                type={"type": "array", "items": {"type": "string"}},
                description="filter by actors' last name id (ex. ?actors=Jo)",
            ),
            OpenApiParameter(
                name="genres",
                type={"type": "array", "items": {"type": "string"}},
                description="filter by genres id (ex. ?genres=concert)",
            ),
            OpenApiParameter(
                name="teams",
                type={"type": "array", "items": {"type": "string"}},
                description="filter by teams id (ex. ?teams=Dynamo)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of events."""
        return super().list(request, *args, **kwargs)


class EventSessionSetPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = "page_size"
    max_page_size = 20


class EventSessionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
    queryset = EventSession.objects.all()
    pagination_class = EventSessionSetPagination

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="event",
                type={"type": "array", "items": {"type": "string"}},
                description="filter by events id (ex. ?event=iron)",
            ),
            OpenApiParameter(
                name="sportarena",
                type={"type": "array", "items": {"type": "string"}},
                description="filter by sportarenas (ex. ?sportarena=stadium)",
            ),
            OpenApiParameter(
                name="show_time",
                type={"type": "array", "items": {"type": "string"}},
                description="filter by event session date id "
                            "(ex. ?show_time=2025-05-11)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Get list of event sessions."""
        return super().list(request, *args, **kwargs)


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
        if self.action == "list":
            return SectionListSerializer
        elif self.action == "retrieve":
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
        if self.action == "list":
            return SportArenaListSerializer
        elif self.action == "retrieve":
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
    page_size_query_param = "page_size"
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
        if self.action == "list":
            serializer = OrderListSerializer
        return serializer
