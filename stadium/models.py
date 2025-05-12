import os
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from django.conf import settings


class SportArena(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'sportarenas'


class Section(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    sportarena = models.ForeignKey(SportArena, on_delete=models.CASCADE, related_name="sections")

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'sections'
        unique_together = ("sportarena", "name")
        ordering = ["sportarena", "name"]


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_sports = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'genres'


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name + " " + self.last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = 'actors'


class Team(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'teams'


def event_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/events/", filename)


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name="event_genres")
    actors = models.ManyToManyField(Actor, blank=True, related_name="event_actors")
    teams = models.ManyToManyField(Team, blank=True, related_name="event_teams")
    image = models.ImageField(null=True, upload_to=event_image_file_path)

    class Meta:
        ordering = ["title"]
        verbose_name_plural = "events"

    def __str__(self):
        return self.title


class EventSession(models.Model):
    show_time = models.DateTimeField()
    sportarena = models.ForeignKey(SportArena, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event")
    sections = models.ManyToManyField(Section, related_name="sections")

    class Meta:
        ordering = ["-show_time"]
        verbose_name_plural = "eventsessions"

    def __str__(self):
        return self.event.title + " " + str(self.show_time)


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    def __str__(self):
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "orders"


class Ticket(models.Model):
    event_session = models.ForeignKey(
        EventSession,
        on_delete=models.CASCADE,
        related_name="ticket_event_sessions"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name="ticket_orders"
    )
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    @staticmethod
    def validate_ticket(attrs, error_to_raise):
        return

        # for ticket_attr_value, ticket_attr_name, section_attr_name in [
        #     (row, "row", "rows"),
        #     (seat, "seat", "seats_in_row"),
        # ]:
        #     count_attrs = getattr(section, section_attr_name)
        #     if not (1 <= ticket_attr_value <= count_attrs):
        #         raise error_to_raise(
        #             {
        #                 ticket_attr_name: f"{ticket_attr_name} "
        #                 f"number must be in available range: "
        #                 f"(1, {section_attr_name}): "
        #                 f"(1, {count_attrs})"
        #             }
        #         )

    def clean(self):
        # self.validate_ticket(
        #     ValidationError,
        # )
        if not (1 <= self.row <= self.section.rows):
            raise ValidationError(
                {
                    "row": f"row must be in range [1, {self.section.rows}], not {self.row} for section {self.section}"
                }
            )
        if not (1 <= self.seat <= self.section.seats_in_row):
            raise ValidationError(
                {
                    "seat": f"seat must be in range [1, {self.section.seats_in_row}], not {self.seat} for section {self.section}"
                }
            )


    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return (
            f"{str(self.event_session)} (section: {self.section.name}, row: {self.row}, seat: {self.seat})"
        )

    class Meta:
        unique_together = ("event_session", "section", "row", "seat")
        ordering = ["section", "row", "seat"]
        verbose_name_plural = "tickets"

