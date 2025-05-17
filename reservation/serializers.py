from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError

from reservation.models import (
    Ticket,
    Order,
)


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if not (1 <= attrs["row"] <= attrs["section"].rows):
            raise serializers.ValidationError(
                {
                    "row": f"row must be in range ["
                    f"1, {attrs["section"].rows}], "
                    f"not {attrs["row"]} for "
                    f"section {attrs["section"]}"
                }
            )
        if not (1 <= attrs["seat"] <= attrs["section"].seats_in_row):
            raise serializers.ValidationError(
                {
                    "seat": f"seat must be in range "
                    f"[1, {attrs["section"].seats_in_row}], "
                    f"not {attrs["seat"]} for "
                    f"section {attrs["section"]}"
                }
            )
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(attrs, ValidationError)
        return data

    class Meta:
        model = Ticket
        fields = ("id", "section", "row", "seat", "event_session")
        unique_together = ("section", "row", "seat", "event_session")


class TicketSeatsSerializer(TicketSerializer):
    section = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    sportarena = serializers.CharField(
        source="section.sportarena.name",
        read_only=True,
    )

    class Meta:
        model = Ticket
        fields = ("sportarena", "section", "row", "seat")


class TicketListSerializer(TicketSerializer):
    from show.serializers import EventSessionListSerializer
    event_session = EventSessionListSerializer(many=False, read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    ticket_orders = TicketSerializer(
        many=True,
        read_only=False,
        allow_empty=False,
    )
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at", "ticket_orders")

    def create_ticket(self, order, ticket_data):
        try:
            Ticket.objects.get_or_create(order=order, **ticket_data)
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)
        # except ValidationError:
        #     print("Ticket not validated")

    def create(self, validated_data):
        tickets_data = validated_data.pop("ticket_orders")
        order = Order.objects.create(**validated_data)

        for ticket_data in tickets_data:
            self.create_ticket(order, ticket_data)

        return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(
        many=True,
        read_only=True,
        source="ticket_orders",
    )
