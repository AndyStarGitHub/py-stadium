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
            actors=self._params_to_ints(actors)
            queryset = queryset.filter(actors__id__in=actors)

        genres = self.request.query_params.get("genres")
        if genres:
            genres=self._params_to_ints(genres)
            queryset = queryset.filter(genres__id__in=genres)

        teams = self.request.query_params.get("teams")
        if teams:
            teams=self._params_to_ints(teams)
            queryset = queryset.filter(teams__id__in=teams)

        if self.action in ("list", "retrieve"):
            return queryset.prefetch_related("genres")
        return queryset

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
