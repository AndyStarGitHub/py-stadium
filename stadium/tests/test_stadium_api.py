import os
import tempfile

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from stadium.models import Event, Genre, Actor, SportArena, EventSession

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
    sportarena = SportArena.objects.create(
        name="Test sportarena"
    )

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
#
#
# def detail_url(event_id):
#     return reverse("stadium:event-detail", args=[event_id])


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



class EVentImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.event = sample_event()
        self.genre = sample_genre()
        self.actor = sample_actor()
        self.event_session = sample_event_session(event=self.event)

    def tearDown(self):
        self.event.image.delete()

    def test_upload_image_to_event(self):
        """Test uploading an image to event"""
        url = image_upload_url(self.event.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(url, {"image": ntf}, format="multipart")
        self.event.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.event.image.path))
#
#     def test_upload_image_bad_request(self):
#         """Test uploading an invalid image"""
#         url = image_upload_url(self.event.id)
#         res = self.client.post(url, {"image": "not image"}, format="multipart")
#
#         self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_post_image_to_event_list(self):
#         url = EVENT_URL
#         with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
#             img = Image.new("RGB", (10, 10))
#             img.save(ntf, format="JPEG")
#             ntf.seek(0)
#             res = self.client.post(
#                 url,
#                 {
#                     "title": "Title",
#                     "description": "Description",
#                     "duration": 90,
#                     "genres": [1],
#                     "actors": [1],
#                     "image": ntf,
#                 },
#                 format="multipart",
#             )
#
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         event = Event.objects.get(title="Title")
#         self.assertFalse(event.image)
#
#     def test_image_url_is_shown_on_event_detail(self):
#         url = image_upload_url(self.event.id)
#         with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
#             img = Image.new("RGB", (10, 10))
#             img.save(ntf, format="JPEG")
#             ntf.seek(0)
#             self.client.post(url, {"image": ntf}, format="multipart")
#         res = self.client.get(detail_url(self.event.id))
#
#         self.assertIn("image", res.data)
#
#     def test_image_url_is_shown_on_event_list(self):
#         url = image_upload_url(self.event.id)
#         with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
#             img = Image.new("RGB", (10, 10))
#             img.save(ntf, format="JPEG")
#             ntf.seek(0)
#             self.client.post(url, {"image": ntf}, format="multipart")
#         res = self.client.get(EVENT_URL)
#
#         self.assertIn("image", res.data[0].keys())
#
#     def test_image_url_is_shown_on_event_session_detail(self):
#         url = image_upload_url(self.event.id)
#         with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
#             img = Image.new("RGB", (10, 10))
#             img.save(ntf, format="JPEG")
#             ntf.seek(0)
#             self.client.post(url, {"image": ntf}, format="multipart")
#         res = self.client.get(EVENT_SESSION_URL)
#
#         self.assertIn("event_image", res.data[0].keys())
