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
            "sportarena",
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name", "is_sports")


class EventListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)


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
            "sportarena",
        )


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ("id", "name")


class EventSessionSerializer(serializers.ModelSerializer):
    event_duration = serializers.CharField(source="event.duration", read_only=True)
    event_title = serializers.CharField(source="event.title", read_only=True)
    event_image = serializers.ImageField(source="event.image", read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    teams = TeamSerializer(many=True, read_only=True)
    # event = EventSerializer()

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
        )


class EventSessionListSerializer(EventSessionSerializer):
    event = EventSerializer()
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
            # "event_title",
            # "event_image",
            "section_name",
            "section_capacity",
            "tickets_available",
        )


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = ("id", "name", "rows", "seats_in_row")


class SportArenaSerializer(serializers.ModelSerializer):

    class Meta:
        model = SportArena
        fields = ("id", "name")


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
