from django.db.models import Q
from django.db.models import Count

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

from .pagination import StandardResultsPagination
from .serializers import PlaceModelSerializer
from places.models import Place

class PlaceListAPIView(generics.ListAPIView):
    serializer_class = PlaceModelSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self, *args, **kwargs):
        qs = Place.objects.all()
        # URL contains "q=", do search
        query = self.request.GET.get("q", None)
        if query:
            qs = qs.filter(name__icontains=query)
        return qs.annotate(trips_count=Count('associated_trips')).order_by("-trips_count").exclude(name="Update Trip Info first to obtain the name of this place.")
