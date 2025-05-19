from django.db import models

from stadium.models import Section, SportArena, event_image_file_path


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_sports = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "genres"


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return self.first_name + " " + self.last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = "actors"


class Team(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "teams"


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name="event_genres")
    actors = models.ManyToManyField(
        Actor,
        blank=True,
        related_name="event_actors"
    )
    teams = models.ManyToManyField(
        Team,
        blank=True,
        related_name="event_teams"
    )
    image = models.ImageField(
        null=True,
        upload_to=event_image_file_path
    )

    class Meta:
        ordering = ["title"]
        verbose_name_plural = "events"

    def __str__(self):
        return self.title


class EventSession(models.Model):
    show_time = models.DateTimeField()
    sportarena = models.ForeignKey(SportArena, on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="event"
    )
    sections = models.ManyToManyField(
        Section,
        related_name="sections"
    )

    class Meta:
        ordering = ["-show_time"]
        verbose_name_plural = "eventsessions"

    def __str__(self):
        return self.event.title + " " + str(self.show_time)
