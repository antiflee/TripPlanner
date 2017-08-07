from datetime import datetime

from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save

import requests
from django.core.files.base import ContentFile      # The image from google static map API is in bytes, so this is needed.
from trips.models import Trip, PlaceVisited
# Create your models here.
class Place(models.Model):
    name                = models.CharField(max_length=140)
    lat                 = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    lng                 = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    associated_trips    = models.ManyToManyField(Trip, through="PlaceDetailInATrip", blank=True, related_name="abstracted_place_list")
    map_image           = models.ImageField(upload_to='places/google_map_images/', default='places/google_map_images/default.png')
    similarPlaces       = models.ManyToManyField('self', through="PlacePlaceSimilarity", blank=True, symmetrical=False, related_name="similar_place_list")
    # image       = models.ImageField(upload_to='places/', default='places/default.jpg')
    # rating      = models.FloatField()

    def __str__(self):
        return str(self.name)

    def get_trips_count(self):
        return Trip.objects.filter(abstracted_place_list=self).count()

    def get_month_distribution(self):
        # Return the frequencies of visiting this place in different years
        placeDetailObjects = PlaceDetailInATrip.objects.filter(place=self).all()
        freq = [0] * 12
        total = 0

        for obj in placeDetailObjects:
            timeArrivalString = datetime.strftime(obj.time_arrival, "%Y-%m-%d")
            month = int(timeArrivalString.split("-")[1]) - 1
            freq[month] += 1
            total += 1

        return freq

    def get_absolute_url(self):
        return reverse("place:detail", kwargs={"pk": self.pk})

    def get_similar_places(self, count=10):
        placePairList = PlacePlaceSimilarity.objects.filter(place1=self).exclude(place2=self).order_by("-similarity")[:count]
        similar_place_list = [placePair.place2 for placePair in placePairList]
        return similar_place_list

class PlaceDetailInATrip(models.Model):
    trip                = models.ForeignKey(Trip)
    place               = models.ForeignKey(Place, related_name="detail_in_a_trip")
    expense             = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    comment             = models.CharField(max_length=140, blank=True)
    lat                 = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    lng                 = models.DecimalField(max_digits=10, decimal_places=7, default=0)
    time_arrival        = models.DateTimeField(auto_now=False)
    # time_departure      = models.DateTimeField(auto_now=False)
    rating              = models.IntegerField(default=0)            # Implement validators later.

class PlacePlaceSimilarity(models.Model):
    place1              = models.ForeignKey(Place, related_name="place1")
    place2              = models.ForeignKey(Place, related_name="place2")
    similarity          = models.PositiveIntegerField(default=0)

GOOGLESTATICMAPAPIKEY = "AIzaSyAWM9aNpToSHrFcVxApdTJh5YK45HG6OFc"   # move it to env var later.

def place_save_receiver(sender, instance, created, *args, **kwargs):
    # Save google map image of the place.
    if created:
        googleStaticMapURL = "https://maps.googleapis.com/maps/api/staticmap?size=635x450&center=" + instance.name \
                            + "&zoom=5&markers=size:mid%7Ccolor:red%7C"+instance.name \
                            + "&key=" + GOOGLESTATICMAPAPIKEY
        # print(googleStaticMapURL)
        response = requests.get(googleStaticMapURL)
        if response.status_code == 200:
            image_filename_prefix = instance.name
            image_content = ContentFile(response.content)
            instance.map_image.save(image_filename_prefix+'.jpg', image_content)

post_save.connect(place_save_receiver, sender=Place)
