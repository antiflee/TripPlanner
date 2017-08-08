from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django import forms
from django.forms.utils import ErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from django.conf import settings
from django.core.files.base import ContentFile      # The image from google static map API is in bytes, so this is needed.
# from django.core.files import File
# from django.core.files.storage import default_storage

from .models import Trip, PlaceVisited, TravelMode
# from .forms import TripModelForm
from .mixins import FormUserNeededMixin

import time
import json
import ast                  # Convert string to dict
import requests
# Create your views here.

GOOGLESTATICMAPAPIKEY = settings.GOOGLESTATICMAPAPIKEY
GOOGLEMAPAPIKEY = settings.GOOGLEMAPAPIKEY
GOOGLEMAPTIMEZONEAPIKEY = settings.GOOGLEMAPTIMEZONEAPIKEY
GENERATED_IMAGE_NAME = 'img.jpg'        # Modify later, to avoid filename conflict of uploaded images.

class TripDetailView(DetailView):
    queryset = Trip.objects.all()
    template_name = "trips/trip_detail.html"

    def get_object(self):
        # print(self.kwargs)
        pk = self.kwargs.get("pk")
        return Trip.objects.get(id=pk)

    def get(self, request, pk):
        trip = get_object_or_404(Trip, pk=pk)
        if trip:
            places = trip.get_place_visted_list()
            # print(places[::-1])
            if request.user.is_authenticated and request.user.trips_liked.filter(pk=pk).exists():
                # print("Already liked")
                liked = True
            else:
                # print("Not liked")
                liked = False
            return render(request, 'trips/trip_detail.html', {'trip': trip,
                                                            'places': places,
                                                            'liked':liked,
                                                            'APIKEY': GOOGLEMAPAPIKEY
                                                            })
        return render(request, "trip:list", {'message': "Trip not found."})

class TripListView(ListView):
    template_name = "trips/trips_list.html"
    queryset = Trip.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(TripListView, self).get_context_data(*args, **kwargs)
        # print(context)
        return context

class TripCreateView(FormUserNeededMixin, CreateView):
    # form_class = TripModelForm
    template_name = 'trips/trip_create.html'
    success_url = "/trip/create"

    def post(self, request):
        # data = request.POST
        # data = json.loads(request.POST.get('json_items'))
        trip_id = -1
        if request.is_ajax():
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = json.loads(request.POST.decode('utf-8'))
        # print(data)
        if request.user.id == int(data['creator_id']):
            if data['mode'] == 'create':
                trip = Trip()
            elif data['mode'] == 'update':
                trip = Trip.objects.get(pk=int(data['trip_id']))
                placesVisited = trip.get_place_visted_list()
                updatePlacePlaceSimilarity(trip,-1)     # If in update mode, we need first decrease the
                                                        # similarities between places in that trip by 1.
                                                        # Then at the end, we incease the similarities of the new places in that trip.
                for placeVisited in placesVisited:
                    placeVisited.delete()

                # Also needs to remove the related Place model.
                trip.abstracted_place_list.clear()

            trip.title                      = data['trip_name']
            # trip.start_date                 = data['start_date']
            trip.start_time                 = data['start_time']
            trip.end_time                   = data['end_time']
            # trip.total_duration_days        = data['total_duration_days']
            trip.time_on_travel_hours       = data['time_on_travel_hours']
            trip.total_distance_meters      = data['total_distance_meters']
            trip.looking_for_partner        = data['looking_for_partner']
            trip.is_public                  = data['is_public']
            trip.description                = data['description']
            trip.creator                    = request.user

            # Deal with default thumbnail.
            googleStaticMapURL = data['googleStaticMapURLWithoutKeyParam'] + GOOGLESTATICMAPAPIKEY
            # print(googleStaticMapURL)
            response = requests.get(googleStaticMapURL)
            if response.status_code == 200:
                # print("status_code == 200")
                image_filename_prefix = request.user.username + "," + data['start_time'] + "," + str(time.time())
                image_content = ContentFile(response.content)
                # path = default_storage.save('tmp/'+GENERATED_IMAGE_NAME, response.content)
                # image = os.path.join(settings.MEDIA_ROOT, path)
                trip.thumbnail_origin.save(image_filename_prefix+'.jpg', image_content)

            trip.save()
            trip_id = trip.id
            # print("trip.created_time is ", trip.created_time)

            friends = data.get('friends', None)
            if friends:
                for friend in friends:
                    pass

            orderIndex = 1
            places = data.get('places', None)
            if places:
                prev_place = None
                for place in places:
                    print('--------------------',place)
                    # place = ast.literal_eval(place)
                    place = json.loads(place)
                    new_place = PlaceVisited()
                    new_place.trip                              = trip
                    new_place.name                              = place['name']
                    new_place.custom_name                       = place['custom_name']
                    new_place.show_suggested_name               = place['show_suggested_name']
                    new_place.is_tag_hidden                     = place['is_tag_hidden']
                    new_place.lat                               = place['latLng']['lat']
                    new_place.lng                               = place['latLng']['lng']
                    new_place.time_zone_dstOffset               = place['time_zone']['dstOffset']
                    new_place.time_zone_rawOffset               = place['time_zone']['rawOffset']
                    # new_place.days_to_stay                      = place['days_to_stay']
                    new_place.prev_place                        = prev_place
                    new_place.travel_mode_to_here               = place['travel_mode_to_here']
                    new_place.travel_time_to_here_sec           = place['travel_time_to_here_sec']
                    new_place.travel_time_to_here_text          = place['travel_time_to_here_text']
                    new_place.travel_dist_to_here_meter         = place['travel_dist_to_here_meter']
                    new_place.travel_dist_to_here_text          = place['travel_dist_to_here_text']
                    new_place.encoded_polyline                  = place['encoded_polyline'].encode('unicode-escape')
                    new_place.time_arrival                      = place['time_arrival']
                    new_place.time_departure                    = place['time_departure']
                    new_place.pin_mode                          = place['pin_mode']
                    new_place.tag_color                         = place['tag_color']
                    # print("time_arrival---------------------------------", new_place.time_arrival)
                    new_place.note                              = place['note']
                    # new_place.encoded_polyline                  = place['encoded_polyline']
                    new_place.order_in_trip                     = orderIndex

                    unavailable_modes = place.get('unavailable_modes', [])

                    new_place.save()

                    for unavailable_mode in unavailable_modes:
                        mode, created = TravelMode.objects.get_or_create(name=unavailable_mode)
                        new_place.unavailable_modes.add(mode)

                    orderIndex += 1
                    prev_place = new_place

            updatePlacePlaceSimilarity(trip, 1)

        if trip_id > 0:
            return JsonResponse({'trip_id':trip.id, 'status':"OK"})
        else:
            return JsonResponse({'trip_id':trip.id, 'status':"Error"})
        # return HttpResponse(json.dumps({'trip_id':trip.id}), content_type='application/json')
        return redirect("trip:list")    # This line is not working, as we use AJAX. The actual redirect occurs in the ajax code in trip_create.html.

    def get(self, request):
        return render(request, 'trips/trip_create.html', {  'user': request.user,
                                                            'update':False,
                                                            'APIKEY': GOOGLEMAPAPIKEY,
                                                            'TIMEZONEAPIKEY': GOOGLEMAPTIMEZONEAPIKEY
                                                            })

class TripUpdateView(UpdateView):
    queryset = Trip.objects.all()
    # form_class = TripModelForm
    template_name = 'trips/trip_create.html'
    # success_url = "/trip/"

    def get_object(self):
        # print(self.kwargs)
        pk = self.kwargs.get("pk")
        return Trip.objects.get(id=pk)

    def get(self, request, pk):
        trip = get_object_or_404(Trip, pk=pk)
        if trip and trip.creator == request.user:
            places = trip.get_place_visted_list()
            return render(request, 'trips/trip_create.html', {
                                                                'trip': trip,
                                                                'places': places,
                                                                'update':True,
                                                                'APIKEY': GOOGLEMAPAPIKEY,
                                                                'TIMEZONEAPIKEY': GOOGLEMAPTIMEZONEAPIKEY})
        return redirect("trip:list")

def tripDelete(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.user.is_authenticated:
        creator = trip.creator
        if request.user == creator:
            trip.delete()
    return redirect("trip:list")

def updatePlacePlaceSimilarity(trip, sign):
    from places.models import PlacePlaceSimilarity
    placeList = trip.abstracted_place_list.all()

    for i in range(len(placeList)-1):
        for j in range(i, len(placeList)):
            place1, place2 = placeList[i], placeList[j]

            placePair, created = PlacePlaceSimilarity.objects.get_or_create(place1=place1, place2=place2)
            placePair.similarity += sign
            placePair.save()

            placePair, created = PlacePlaceSimilarity.objects.get_or_create(place1=place2, place2=place1)
            placePair.similarity += sign
            placePair.save()


# @login_required
# def tripCreate(request):
#     if request.method == "POST":
#         # data = request.POST
#         # data = json.loads(request.POST.get('json_items'))
#         if request.is_ajax():
#             data = json.loads(request.body.decode('utf-8'))
#         else:
#             data = json.loads(request.POST.decode('utf-8'))
#         # print(data)
#         if request.user.id == int(data['creator_id']):
#             trip = Trip()
#             trip.title = data['trip_name']
#             trip.start_date = data['start_date']
#             trip.total_duration_days = data['total_duration_days']
#             trip.time_on_travel_hours = data['time_on_travel_hours']
#             trip.creator = request.user
#             trip.save()
#
#             friends = data.get('friends', None)
#             if friends:
#                 for friend in friends:
#                     pass
#
#             orderIndex = 1
#             places = data.get('places', None)
#             if places:
#                 for place in places:
#                     place = ast.literal_eval(place)
#                     new_place = PlaceVisited()
#                     new_place.trip = trip
#                     new_place.displayed_name = place['displayed_name']
#                     new_place.lat = place['latLng']['lat']
#                     new_place.lng = place['latLng']['lng']
#                     new_place.days_to_stay = place['days_to_stay']
#                     new_place.travel_mode_to_here = place['travel_mode_to_here']
#                     new_place.travel_time_to_here_sec = place['travel_time_to_here_sec']
#                     new_place.travel_time_to_here_text = place['travel_time_to_here_text']
#                     new_place.travel_dist_to_here_meter = place['travel_dist_to_here_meter']
#                     new_place.travel_dist_to_here_text = place['travel_dist_to_here_text']
#                     new_place.order_in_trip = orderIndex
#                     new_place.save()
#
#                     orderIndex += 1
#
#         return redirect("trip:list")    # This line is not working, as we use AJAX. The actual redirect occurs in the ajax code in trip_create.html.
#     else:
#         return render(request, 'trips/trip_create.html', {'user': request.user})

# def tripDetail(request, pk):
#     trip = get_object_or_404(Trip, pk=pk)
#     if trip:
#         places = trip.get_place_visted_list()
#         return render(request, 'trips/trip_detail.html', {'trip': trip, 'places': places})
#     return render(request, "trip:list", {'message': "Trip not found."})
