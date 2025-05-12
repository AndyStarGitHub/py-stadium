from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from stadium.models import Genre, SportArena, Section, Actor, Team, Event, EventSession, Ticket, Order


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


class SectionSerializer(serializers.ModelSerializer):
    sportarena = serializers.PrimaryKeyRelatedField(queryset=SportArena.objects.all())

    class Meta:
        model = Section
        fields = ("id", "sportarena", "name", "rows", "seats_in_row")


class SportArenaSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = SportArena
        fields = ("id", "name", "sections")


class SportArenaListSerializer(SportArenaSerializer):
    sections = serializers.SlugRelatedField(
        slug_field="name",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Section
        fields = ("id", "name", "sections",)


class SportArenaRetrieveSerializer(SportArenaSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = SportArena
        fields = ("id", "name", "sections")


class SectionRetrieveSerializer(SectionSerializer):
    sportarena = SportArenaSerializer()

class SectionListSerializer(SectionSerializer):
    sportarena = serializers.SlugRelatedField(
        slug_field="name",
        many=False,
        read_only=True,
    )

    class Meta:
        model = Section
        fields = ("id", "name", "rows", "seats_in_row", "sportarena",)


class EventSessionSerializer(serializers.ModelSerializer):
    event_duration = serializers.CharField(source="event.duration", read_only=True)
    event_title = serializers.CharField(source="event.title", read_only=True)
    event_image = serializers.ImageField(source="event.image", read_only=True)
    sportarena = serializers.PrimaryKeyRelatedField(queryset=SportArena.objects.all())

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
    event_title = serializers.CharField(source="event.title", read_only=True)
    event_image = serializers.ImageField(source="event.image", read_only=True)
    sportarena = serializers.SlugRelatedField(
        slug_field="name",
        many=False,
        read_only=True,
    )
    sections = serializers.SlugRelatedField(
        slug_field="name",
        many=True,
        read_only=True,
    )

    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = EventSession
        fields = (
            "id",
            "show_time",
            "sections",
            "sportarena",
            "actors",
            "genres",
            "teams",
            "event_title",
            "event_image",
        )


class EventSessionRetrieveSerializer(EventSessionSerializer):

    event = EventListSerializer()
    sportarena = SportArenaSerializer()

    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    teams = TeamSerializer(many=True, read_only=True)

    event_title = serializers.CharField(source="event.title", read_only=True)
    event_image = serializers.ImageField(source="event.image", read_only=True)
    section_name = serializers.CharField(
        source="section.name", read_only=True
    )
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
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs.get("row"),
            attrs.get("seat"),
            attrs.get("section"),
            ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "section", "row", "seat", "event_session")


class TicketListSerializer(TicketSerializer):
    event_session = EventSessionListSerializer(many=False, read_only=True)


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("section", "row", "seat")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(
        many=True,
        read_only=False,
        allow_empty=False,
        source="ticket_orders",
    )

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("ticket_orders")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(
        many=True,
        read_only=True,
        source="ticket_orders",
    )
