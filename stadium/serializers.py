from rest_framework import serializers

from stadium.models import Genre, SportArena, Section, Actor, Team


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


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


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("id", "name")