import re
from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.urls import reverse
from django.db import models

from datetime import timedelta

import requests
# from places.models import Place
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

# Create your models here.

User        = get_user_model()
DRIVING     = 'Driving'
TRANSIT     = 'Transit'
WALKING     = 'Walking'
CYCLING     = 'Cycling'
FLIGHT      = 'Flight'
START       = 'START'

TRAVEL_MODE_CHOICES = (
    (DRIVING, 'DRIVING'),
    (TRANSIT, 'TRANSIT'),
    (WALKING, 'WALKING'),
    (CYCLING, 'BICYCLING'),
    # (FLIGHT,  'FLIGHT'),
    (START,   'START'),
)

PRIMARY = 'label label-primary'
SUCCESS = 'label label-success'
INFO    = 'label label-info'
WARNING = 'label label-warning'
DANGER  = 'label label-danger'
DEFAULT = 'label label-default'

TAG_COLOR_CHOICES = (
    (PRIMARY, 'label label-primary'),
    (SUCCESS, 'label label-success'),
    (INFO,    'label label-info'),
    (WARNING, 'label label-warning'),
    (DANGER,  'label label-danger'),
    (DEFAULT, 'label label-default'),
)

NEITHER = 'neither'
DEPARTURE = 'departure'
DURATION = 'duration'

PIN_MODE_CHOICES = (
    (NEITHER, 'neither'),
    (DEPARTURE, 'departure'),
    (DURATION, 'duration'),
)

class TripManager(models.Manager):
    def like_toggle(self, user, trip_obj):
        if user in trip_obj.people_liked_this.all():
            is_liked = False
            trip_obj.people_liked_this.remove(user)
        else:
            is_liked = True
            trip_obj.people_liked_this.add(user)
        return is_liked

class Trip(models.Model):
    title                   = models.CharField(max_length=140)
    creator                 = models.ForeignKey(User, related_name="trips", null=True)
    friends                 = models.ManyToManyField(User, related_name="involved_trips", blank=True)
    group_size              = models.PositiveIntegerField(default=1)
    # start_date              = models.DateField(auto_now=False)
    start_time              = models.DateTimeField(auto_now=False)
    end_time                = models.DateTimeField(auto_now=False)
    total_duration_days     = models.PositiveIntegerField(default=1)
    total_distance_meters   = models.PositiveIntegerField(default=0)
    time_on_travel_hours    = models.PositiveIntegerField(default=0)
    created_time            = models.DateTimeField(auto_now=True)
    updated_time            = models.DateTimeField(auto_now=True)
    looking_for_partner     = models.BooleanField(default=False)
    description             = models.TextField(max_length=3000, blank=True)
    op_comment              = models.TextField(max_length=3000, blank=True)
    # comments =
    is_finished             = models.BooleanField(default=False)        # Only visible to 'creator'+'friends' if False; public otherwise.
    is_public               = models.BooleanField(default=True)
    people_liked_this       = models.ManyToManyField(User, related_name="trips_liked", blank=True)
    thumbnail_origin        = models.ImageField(upload_to='thumbnails/', default='thumbnails/default.jpg')
    thumbnail_resized       = ImageSpecField(source='thumbnail_origin',
                                              processors=[ResizeToFill(100, 50)],
                                              format='JPEG',
                                              options={'quality': 60})
    objects = TripManager()

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse("trip:detail", kwargs={"pk": self.pk})

    def get_total_dist_miles(self):
        return int(self.total_distance_meters / 1609.34)

    def get_likes_count(self):
        return User.objects.filter(trips_liked=self).count()

    def get_group_size(self):
        return 1 + User.objects.filter(involved_trips=self).count()

    def get_group_size_formatted(self):
        num = self.get_group_size()
        return str(num) + " people" if num > 1 else "1 person"

    def get_place_visted_list(self):
        return PlaceVisited.objects.filter(trip=self)

    def get_start_date_yyyymmdd(self):
        return datetime.strftime(self.start_time, "%Y-%m-%d")

    def get_end_date_yyyymmdd(self):
        return datetime.strftime(self.end_time, "%Y-%m-%d")


    # def get_start_date_yyyymmdd(self):
    #     print(datetime.strftime(self.start_date, "%Y-%m-%d"))
    #     return datetime.strftime(self.start_date, "%Y-%m-%d")

class TravelMode(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class PlaceVisited(models.Model):
    trip                        = models.ForeignKey(Trip, related_name="places_visited", on_delete=models.CASCADE)
    name                        = models.CharField(max_length=140, blank=True)
    custom_name                 = models.CharField(max_length=140, blank=True)
    show_suggested_name         = models.BooleanField(default=False)
    # place                       = models.ForeignKey(Place)
    lat                         = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    lng                         = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    # days_to_stay                = models.IntegerField(default=0)
    time_zone_rawOffset         = models.IntegerField(default=-28800)
    time_zone_dstOffset         = models.IntegerField(default=3600)                 # Daylight time or not, unit in seconds.
    prev_place                  = models.ForeignKey('self', related_name="next_place", null=True, default=None, on_delete=models.CASCADE)
    travel_mode_to_here         = models.CharField(max_length=10, choices=TRAVEL_MODE_CHOICES, default=START)
    travel_time_to_here_sec     = models.PositiveIntegerField(default=0)
    travel_time_to_here_text    = models.CharField(max_length=140, blank=True)
    travel_dist_to_here_meter   = models.PositiveIntegerField(default=0)
    travel_dist_to_here_text    = models.CharField(max_length=140, blank=True)
    encoded_polyline            = models.CharField(max_length=4000, blank=True)
    unavailable_modes           = models.ManyToManyField(TravelMode, related_name="not_available_in", blank=True)
    time_arrival                = models.DateTimeField(auto_now=False)
    time_departure              = models.DateTimeField(auto_now=False)
    # is_pinned                   = models.BooleanField(default=False)                # Whether the time_arrival and time_departure are fixed so that it won't be autoset if there is a time conflict.
    pin_mode                    = models.CharField(max_length=20, choices=PIN_MODE_CHOICES, default=NEITHER)
    tag_color                   = models.CharField(max_length=20, choices=TAG_COLOR_CHOICES, default=PRIMARY)
    is_tag_hidden               = models.BooleanField(default=False)
    note                        = models.CharField(max_length=3000, blank=True)
    # encoded_polyline            = models.CharField(max_length=1500, blank=True)
    order_in_trip               = models.PositiveIntegerField(default=0)
    expense                     = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    comment                     = models.CharField(max_length=140, blank=True)
    rating                      = models.IntegerField(default=0)            # Implement validators later.
    # date_arrival
    # weatherArrival
    # weatherDeparture

    @property
    def expense(self):
        return "$%s" % self.expense     # Add a dollar sign in front of the money amount.

    def __str__(self):
        return self.name + ", of " + str(self.trip)

    def get_time_arrival(self):
        return datetime.strftime(self.time_arrival, "%Y-%m-%d %H:%M:%S")

    def get_time_departure(self):
        return datetime.strftime(self.time_departure, "%Y-%m-%d %H:%M:%S")

    def get_unavailable_modes_list(self):
        result = [mode.name for mode in self.unavailable_modes.all()]
        # for mode in self.unavailable_modes.all():
        #     result += mode.name + ", "
        # if len(result) > 0:
        #     result = result[:-2]
        return result

def post_save_place_receiver(sender, instance, created, *args, **kwargs):
    if created:
        from places.models import Place, PlaceDetailInATrip, PlacePlaceSimilarity
        trip = instance.trip
        place, place_created = Place.objects.get_or_create(name=instance.name)
        if place_created or (place.lat == 0 and place.lng == 0):
            lat, lng = get_lat_lng_from_name(instance.name)
            place.lat = lat
            place.lng = lng
            place.save()
        if place_created or not (trip.abstracted_place_list.filter(name=instance.name).exists()):
            placeTripRelationShip = PlaceDetailInATrip(
                                                        trip            = instance.trip,
                                                        place           = place,
                                                        lat             = instance.lat,
                                                        lng             = instance.lng,
                                                        time_arrival    = instance.time_arrival
                                                        # date_arrival = instance.get_date_arrival()
                                                    )
            placeTripRelationShip.save()

        # if instance.next_place == None:
        #     # The last place in the trip has been saved. We can now update the similarity between places.
        #     placesInvolved = []
        #     curPlaceVisited = instance
        #     while curPlaceVisited:
        #         place, place_created = Place.objects.get_or_create(name=curPlaceVisited.name)
        #         placesInvolved.append(place)
        #         curPlace

def get_lat_lng_from_name(name):
    urlPrefix = "https://maps.googleapis.com/maps/api/geocode/json?address="
    APIKEY = "AIzaSyAoX1pdP9-vueaY2JVmIxViYdUdY1DbHJM"
    googleGeoCodingUrl = urlPrefix + name + "&key=" + APIKEY
    # print(name, googleGeoCodingUrl)
    response = requests.get(googleGeoCodingUrl)
    # print(response)
    if response.status_code == 200:
        results = response.json()
        lat = results['results'][0]['geometry']['location']['lat']
        lng = results['results'][0]['geometry']['location']['lng']
        return lat, lng
    return 0, 0


post_save.connect(post_save_place_receiver, sender=PlaceVisited)


def trip_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        # notify a user
        user_regex = r'@(?P<username>[\w.@+-]+)'
        usernames = re.findall(user_regex, instance.op_comment)
        # send notification to user here.

        hash_regex = r'#(?P<hashtag>[\w.d-]+)'
        hashtags = re.findall(hash_regex, instance.op_comment)
        # send hashtag signal to user here.

post_save.connect(trip_save_receiver, sender=Trip)
