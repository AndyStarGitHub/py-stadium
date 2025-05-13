from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

ACTOR_URL = reverse("stadium:actor-list")
EVENT_URL = reverse("stadium:event-list")
EVENT_SESSION_URL = reverse("stadium:eventsession-list")
SPORTARENA_URL = reverse("stadium:sportarena-list")


class UnauthenticatedEventApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(EVENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UnauthenticatedEventSessionApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(EVENT_SESSION_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UnauthenticatedSportArenasApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(SPORTARENA_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UnauthenticatedActorsApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ACTOR_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
