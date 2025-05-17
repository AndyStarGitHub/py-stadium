from rest_framework import serializers


from show.models import (
    Genre,
    Actor,
    Team,
    Event,
    EventSession,
)

from stadium.serializers import (
    SportArenaSerializer,
)

from stadium.models import SportArena


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "duration",
            "genres",
            "actors",
            "teams",
            "image",
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name", "is_sports")


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ("id", "name")


class EventListSerializer(serializers.ModelSerializer):
    actors = serializers.SlugRelatedField(
        slug_field="full_name",
        many=True,
        read_only=True,
    )
    genres = serializers.SlugRelatedField(
        slug_field="name",
        many=True,
        read_only=True,
    )
    teams = serializers.SlugRelatedField(
        slug_field="name",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "duration",
            "genres",
            "actors",
            "teams",
            "image",
        )


class EventRetrieveSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "duration",
            "genres",
            "actors",
            "teams",
            "image",
        )


class EventSessionSerializer(serializers.ModelSerializer):
    event_duration = serializers.CharField(
        source="event.duration",
        read_only=True
    )
    event_title = serializers.CharField(
        source="event.title",
        read_only=True
    )
    event_image = serializers.ImageField(
        source="event.image",
        read_only=True
    )
    sportarena = serializers.PrimaryKeyRelatedField(
        queryset=SportArena.objects.all()
    )

    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = EventSession
        fields = (
            "id",
            "event",
            "event_title",
            "show_time",
            "event_duration",
            "genres",
            "actors",
            "teams",
            "event_image",
            "sections",
            "sportarena",
        )


class EventSessionListSerializer(EventSessionSerializer):
    tickets_reserved = serializers.SerializerMethodField()
    tickets_available = serializers.SerializerMethodField()
    event_title = serializers.CharField(source="event.title", read_only=True)
    event_image = serializers.ImageField(source="event.image", read_only=True)
    sportarena = serializers.SlugRelatedField(
        slug_field="name",
        many=False,
        read_only=True,
    )
    sportarena_capacity = serializers.IntegerField(
        source="sportarena.sportarena_capacity", read_only=True
    )

    sections = serializers.SlugRelatedField(
        slug_field="name",
        many=True,
        read_only=True,
    )

    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    teams = TeamSerializer(many=True, read_only=True)

    def get_tickets_reserved(self, obj):
        return obj.ticket_event_sessions.count()

    def get_sportarena_capacity(self, obj):
        return obj.sportarena.sportarena_capacity

    def get_tickets_available(self, obj):
        return (self.get_sportarena_capacity(obj)
                - self.get_tickets_reserved(obj))

    class Meta:
        model = EventSession
        fields = (
            "id",
            "show_time",
            "sections",
            "sportarena",
            "sportarena_capacity",
            "tickets_reserved",
            "tickets_available",
            "actors",
            "genres",
            "teams",
            "event_title",
            "event_image",
        )


class EventSessionRetrieveSerializer(EventSessionSerializer):
    from reservation.serializers import TicketSeatsSerializer
    event = EventListSerializer(many=False)
    sportarena = SportArenaSerializer(many=False)

    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    teams = TeamSerializer(many=True, read_only=True)

    event_title = serializers.CharField(source="event.title", read_only=True)
    event_image = serializers.ImageField(source="event.image", read_only=True)
    tickets = TicketSeatsSerializer(
        many=True,
        read_only=True,
        source="ticket_event_sessions",
    )

    section_name = serializers.CharField(source="section.name", read_only=True)
    section_capacity = serializers.IntegerField(
        source="section.capacity", read_only=True
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = EventSession
        fields = (
            "id",
            "event",
            "show_time",
            "section_name",
            "section_capacity",
            "tickets_available",
            "sportarena",
            "actors",
            "genres",
            "teams",
            "tickets",
        )
