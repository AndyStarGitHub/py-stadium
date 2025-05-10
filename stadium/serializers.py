from rest_framework import serializers

from stadium.models import Genre, SportArena


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name", "is_sports")


class GenreDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = (
            "id",
            "name",
            "is_sports",
        )


class SportArenaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportArena
        fields = ("id", "name")