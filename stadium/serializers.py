from rest_framework import serializers

from stadium.models import Genre, SportArena, Section, Actor, Team, Event, EventSession


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "duration",
            "genres",
            "actors",
            "teams",
            "image",
            "sportarena",
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name", "is_sports")


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ("id", "name")


class EventSessionSerializer(serializers.ModelSerializer):
    event_duration = serializers.CharField(source="event.duration", read_only=True)
    event_title = serializers.CharField(source="event.title", read_only=True)
    event_image = serializers.ImageField(source="event.image", read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = EventSession
        fields = (
            "id",
            "event",
            "event_title",
            "show_time",
            "event_duration",
            "genres",
            "actors",
            "teams",
            "event_image",
            "sections",
        )


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = ("id", "name", "rows", "seats_in_row")


class SportArenaSerializer(serializers.ModelSerializer):

    class Meta:
        model = SportArena
        fields = ("id", "name")
