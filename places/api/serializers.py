from rest_framework import serializers
from places.models import Place, PlaceDetailInATrip
from trips.api.serializers import TripModelSerializer

class PlaceDetailInATripSerializer(serializers.ModelSerializer):
    trip_id = serializers.ReadOnlyField(source='trip.id')
    trip_name = serializers.ReadOnlyField(source='trip.title')

    class Meta:
        model = PlaceDetailInATrip
        fields = [
            'trip_id',
            'trip_name',
            'expense',
            'rating',
            'comment',
        ]


class PlaceModelSerializer(serializers.ModelSerializer):
    trips_count = serializers.SerializerMethodField()
    # associated_trips  = PlaceDetailInATripSerializer(many=True)
    associated_trips = PlaceDetailInATripSerializer(source='detail_in_a_trip', many=True)
    similar_places = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = [
            'id',
            'name',
            'map_image',
            'trips_count',
            'lat',
            'lng',
            'similar_places',
            'associated_trips',
        ]

    def get_trips_count(self, obj):
        return obj.get_trips_count()

    def get_similar_places(self, obj, count=10):
        place_list = obj.get_similar_places(count)
        return [place.name for place in place_list]
