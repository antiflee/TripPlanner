from rest_framework import serializers
from accounts.api.serializers import UserDisplaySerializer

from trips.models import Trip, PlaceVisited, TravelMode

class TravelModeModelSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = TravelMode
        fields = [
                'name',
                ]

    def get_name(self, obj):
        return obj.name.upper()

class PlaceVisitedModelSerializer(serializers.ModelSerializer):
    time_arrival = serializers.SerializerMethodField()
    time_departure = serializers.SerializerMethodField()
    unavailable_modes = TravelModeModelSerializer(many=True)
    prev_place = serializers.SerializerMethodField()
    class Meta:
        model = PlaceVisited
        exclude = [
            'id',
            'trip',
            'order_in_trip',
        ]

    def get_time_arrival(self, obj):
        print(obj.get_time_arrival())
        return obj.get_time_arrival()

    def get_time_departure(self, obj):
        return obj.get_time_departure()

    def get_prev_place(self, obj):
        return obj.prev_place.custom_name if obj.prev_place else ""

    # def get_note_to_here(self, obj):
    #     request = self.context.get("request")
    #     user = request.user
    #     if user == obj.trip.creator:
    #         return obj.note_to_here
    #     return ""
    #
    # def get_note_in_here(self, obj):
    #     request = self.context.get("request")
    #     user = request.user
    #     if user == obj.trip.creator:
    #         return obj.note_in_here
    #     return None

class TripModelSerializer(serializers.ModelSerializer):
    creator         = UserDisplaySerializer(read_only=True)
    places_visited  = PlaceVisitedModelSerializer(many=True)
    likes           = serializers.SerializerMethodField()
    did_like        = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = [
            'id',
            'title',
            'creator',
            'start_time',
            'end_time',
            'total_duration_days',
            'places_visited',
            'likes',
            'did_like',
            'thumbnail_origin',
            'looking_for_partner',
            'description',
            # 'thumbnail_resized',
        ]

    def get_likes(self, obj):
        return obj.get_likes_count()

    def get_did_like(self, obj):
        request = self.context.get("request")
        user = request.user
        if user.is_authenticated():
            if user in obj.people_liked_this.all():
                return True
        return False
