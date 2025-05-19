from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from show.models import Event, Genre, Actor, EventSession
from stadium.models import SportArena

ACTOR_URL = reverse("stadium:actor-list")
EVENT_URL = reverse("stadium:event-list")
EVENT_SESSION_URL = reverse("stadium:eventsession-list")
SPORTARENA_URL = reverse("stadium:sportarena-list")


def sample_event(**params):
    defaults = {
        "title": "Sample event",
        "description": "Sample event description",
        "duration": 90,
    }
    defaults.update(params)

    return Event.objects.create(**defaults)


def sample_genre(**params):
    defaults = {
        "name": "Test genre",
    }
    defaults.update(params)

    return Genre.objects.create(**defaults)


def sample_actor(**params):
    defaults = {"first_name": "Stanislav", "last_name": "Boklan"}
    defaults.update(params)

    return Actor.objects.create(**defaults)


def sample_event_session(**params):
    sportarena = SportArena.objects.create(name="Test sportarena")

    defaults = {
        "show_time": "2025-05-14 14:00:00",
        "event": None,
        "sportarena": sportarena,
    }
    defaults.update(params)

    return EventSession.objects.create(**defaults)


def image_upload_url(event_id):
    """Return URL for the image upload"""
    return reverse("stadium:event-upload-image", args=[event_id])


class UnauthenticatedSportArenasApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(SPORTARENA_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
