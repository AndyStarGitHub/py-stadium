from django.core.exceptions import ValidationError
from django.db import models

from django.conf import settings

from show.models import EventSession
from stadium.models import Section


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
        Order, on_delete=models.CASCADE, related_name="ticket_orders"
    )
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    @staticmethod
    def validate_ticket(attrs, error_to_raise):
        return

    def clean(self):
        if not (1 <= self.row <= self.section.rows):
            raise ValidationError(
                {
                    "row": f"row must be in range [1, {self.section.rows}], "
                    f"not {self.row} for section {self.section}"
                }
            )
        if not (1 <= self.seat <= self.section.seats_in_row):
            raise ValidationError(
                {
                    "seat": f"seat must be in range "
                    f"[1, {self.section.seats_in_row}], "
                    f"not {self.seat} for section {self.section}"
                }
            )
        if self.section not in self.event_session.sections.all():
            raise ValidationError(
                {
                    "section": f"The section {self.section.name} doesn't belong to the event venue sport arena {self.event_session.sportarena.name}"
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
        return (f"{str(self.event_session)} "
                f"(section: {self.section.name}, "
                f"row: {self.row}, seat: {self.seat})")

    class Meta:
        unique_together = ("event_session", "section", "row", "seat")
        ordering = ["section", "row", "seat"]
        verbose_name_plural = "tickets"
