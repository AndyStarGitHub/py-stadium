from rest_framework import serializers

from stadium.models import Genre, SportArena, Section


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name", "is_sports")


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ("id", "name", "rows", "seats_in_row")


class SportArenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportArena
        fields = ("id", "name")