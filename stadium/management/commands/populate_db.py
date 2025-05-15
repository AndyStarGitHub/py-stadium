from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker
import random

from stadium.models import Genre, Team, Actor, Event, EventSession, SportArena, Section, Ticket, Order

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with fake data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Generating fake data...")

        for _ in range(1):
            genre = Genre.objects.create(name=fake.word())

        for _ in range(1):
            team = Team.objects.create(name=fake.company())

        for _ in range(1):
            actor = Actor.objects.create(first_name=fake.first_name(), last_name=fake.last_name())

        for _ in range(1):
            event = Event.objects.create(
                title=fake.catch_phrase(),
                description=fake.text(),
                duration=100,
                image=None
            )
            event.genres.set(Genre.objects.order_by('?')[:2])
            event.teams.set(Team.objects.order_by('?')[:2])
            event.actors.set(Actor.objects.order_by('?')[:2])

        for _ in range(1):
            arena = SportArena.objects.create(
                name=fake.city() + " Arena",
            )

        for event in Event.objects.all():
            EventSession.objects.create(
                event=event,
                sportarena=SportArena.objects.order_by('?').first(),
                show_time=fake.future_datetime(end_date="+30d"),
            )

        for sportarena in SportArena.objects.all():
            Section.objects.create(
                sportarena=sportarena,
                name=fake.catch_phrase(),
                rows = random.randint(10, 20),
                seats_in_row = random.randint(8, 15),
            )

        User = get_user_model()
        user = User.objects.first()
        for section in Section.objects.all():
            for event_session in EventSession.objects.all():
                order=Order.objects.create(
                    user=user,
                )
                for _ in range(3):
                        Ticket.objects.get_or_create(
                            order=order,
                            event_session=event_session,
                            section=section,
                            row=random.randint(1,10),
                            seat=random.randint(1, 8),
                        )

        self.stdout.write(self.style.SUCCESS("Fake data successfully generated!"))
