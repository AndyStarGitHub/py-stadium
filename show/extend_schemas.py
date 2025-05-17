# show/docs/event_schema_docs.py
from drf_spectacular.utils import extend_schema, OpenApiParameter

event_list_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name="actors",
            type={"type": "array", "items": {"type": "string"}},
            description="filter by actors' last name id (ex. ?actors=Jo)",
        ),
        OpenApiParameter(
            name="genres",
            type={"type": "array", "items": {"type": "string"}},
            description="filter by genres id (ex. ?genres=concert)",
        ),
        OpenApiParameter(
            name="teams",
            type={"type": "array", "items": {"type": "string"}},
            description="filter by teams id (ex. ?teams=Dynamo)",
        ),
    ]
)

event_session_list_schema = extend_schema(
    parameters=[
        OpenApiParameter(
            name="event",
            type={"type": "array", "items": {"type": "string"}},
            description="filter by events id (ex. ?event=iron)",
        ),
        OpenApiParameter(
            name="sportarena",
            type={"type": "array", "items": {"type": "string"}},
            description="filter by sportarenas (ex. ?sportarena=stadium)",
        ),
        OpenApiParameter(
            name="show_time",
            type={"type": "array", "items": {"type": "string"}},
            description="filter by event session date id "
                        "(ex. ?show_time=2025-05-11)",
        ),
    ]
)
