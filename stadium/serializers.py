from rest_framework import serializers

from stadium.models import (
    SportArena,
    Section,
)


class SectionSerializer(serializers.ModelSerializer):
    sportarena = serializers.PrimaryKeyRelatedField(
        queryset=SportArena.objects.all()
    )

    class Meta:
        model = Section
        fields = (
            "id",
            "sportarena",
            "name",
            "rows",
            "seats_in_row"
        )


class SportArenaSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = SportArena
        fields = ("id", "name", "sections")


class SportArenaListSerializer(SportArenaSerializer):
    sections = serializers.SlugRelatedField(
        slug_field="name",
        many=True,
        read_only=True,
    )
    sportarena_capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Section
        fields = ("id", "name", "sections", "sportarena_capacity")


class SportArenaRetrieveSerializer(SportArenaSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = SportArena
        fields = ("id", "name", "sections")


class SectionRetrieveSerializer(SectionSerializer):
    sportarena = SportArenaSerializer()


class SectionListSerializer(SectionSerializer):
    sportarena = serializers.SlugRelatedField(
        slug_field="name",
        many=False,
        read_only=True,
    )
    capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Section
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "sportarena",
            "capacity"
        )
