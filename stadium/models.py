import os
import uuid

from django.utils.text import slugify

from django.db import models


def event_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/events/", filename)


class SportArena(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    @property
    def sportarena_capacity(self):
        return sum(section.capacity for section in self.sections.all())

    class Meta:
        verbose_name_plural = "sportarenas"


class Section(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    sportarena = models.ForeignKey(
        SportArena, on_delete=models.CASCADE, related_name="sections"
    )

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "sections"
        unique_together = ("sportarena", "name")
        ordering = ["sportarena", "name"]
