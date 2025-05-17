from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker
import random

from stadium.models import (
    Genre,
    Team,
    Actor,
    Event,
    EventSession,
    SportArena,
    Section,
)

from reservation.models import (
    Ticket,
    Order,
)

fake = Faker()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating fake data...")

        # Ticket.objects.all().delete()
        # Order.objects.all().delete()
        # EventSession.objects.all().delete()
        # Event.objects.all().delete()
        # Genre.objects.all().delete()
        # Team.objects.all().delete()
        # Actor.objects.all().delete()
        # Section.objects.all().delete()
        # SportArena.objects.all().delete()

        for _ in range(4):
            Genre.objects.create(name=fake.word())

        for _ in range(6):
            Team.objects.create(name=fake.company())

        for _ in range(12):
            Actor.objects.create(
                first_name=fake.first_name(), last_name=fake.last_name()
            )

        for _ in range(6):
            event = Event.objects.create(
                title=fake.catch_phrase(),
                description=fake.text(),
                duration=100,
                image=None,
            )
            event.genres.set(Genre.objects.order_by("?")[:2])
            event.teams.set(Team.objects.order_by("?")[:2])
            event.actors.set(Actor.objects.order_by("?")[:2])

        for _ in range(4):
            SportArena.objects.create(
                name=fake.city() + " Arena",
            )

        for sportarena in SportArena.objects.all():
            for _ in range(5):
                Section.objects.create(
                    sportarena=sportarena,
                    name=fake.catch_phrase(),
                    rows=random.randint(10, 20),
                    seats_in_row=random.randint(15, 30),
                )

        for _ in range(3):
            for event in Event.objects.all():
                sportarena = SportArena.objects.order_by("?").first()
                event_session = EventSession.objects.create(
                    event=event,
                    sportarena=sportarena,
                    show_time=fake.future_datetime(end_date="+30d"),
                )
                event_session.sections.set(sportarena.sections.all())

        user_mod = get_user_model()
        user = user_mod.objects.first()
        for section in Section.objects.all():
            for event_session in EventSession.objects.all():
                order = Order.objects.create(
                    user=user,
                )
                for _ in range(5):
                    Ticket.objects.get_or_create(
                        order=order,
                        event_session=event_session,
                        section=section,
                        row=random.randint(1, 10),
                        seat=random.randint(1, 8),
                    )

        success_message = "Fake data successfully generated!"
        self.stdout.write(self.style.SUCCESS(success_message))
