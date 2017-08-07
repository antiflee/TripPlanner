from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from .models import Place, PlaceDetailInATrip
# Create your views here.

class PlaceListView(ListView):
    template_name = "places/places_list.html"
    queryset = Place.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(PlaceListView, self).get_context_data(*args, **kwargs)
        # print(context)
        return context

class PlaceDetailView(DetailView):
    queryset = Place.objects.all()
    template_name = "places/place_detail.html"

    def get_object(self):
        # print(self.kwargs)
        pk = self.kwargs.get("pk")
        return Place.objects.get(id=pk)

    def get(self, request, pk):
        place = get_object_or_404(Place, pk=pk)
        if place:
            place_detail_in_a_trip = PlaceDetailInATrip.objects.filter(place=place).annotate(trip_popularity=Count('trip__people_liked_this')).order_by('-trip_popularity')[:10]
            # print(place_detail_in_a_trip.query)
            return render(request, 'places/place_detail.html', {'place': place, 'details':place_detail_in_a_trip})
        return render(request, "places:list", {'message': "Place not found."})

class PlaceHeatmapView(ListView):
    queryset = Place.objects.all()
    template_name = "places/place_heatmap.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PlaceHeatmapView, self).get_context_data(*args, **kwargs)
        # print(context)
        return context
