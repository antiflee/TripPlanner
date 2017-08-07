from django.db.models import Q
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response

from .pagination import StandardResultsPagination
from .serializers import TripModelSerializer
from trips.models import Trip

User        = get_user_model()

class TripListAPIView(generics.ListAPIView):
    serializer_class = TripModelSerializer
    pagination_class = StandardResultsPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self, *args, **kwargs):
        # URL contains "username="
        requested_user = self.kwargs.get("username")
        trips_this_user_liked = self.request.GET.get("trips_this_user_liked", False)
        if requested_user:
            # If the query arguments contain "username".
            if trips_this_user_liked == 'true':
                # Only needs trips this user liked
                qs = get_object_or_404(User, username=requested_user).trips_liked.all()
            else:
                # The URL that requests the listAPIView contains a username. Used when viewing all trips belong to that user.
                qs = Trip.objects.filter(creator__username=requested_user)
        else:
            qs = Trip.objects.all()

        # URL contains "q=", do search
        query = self.request.GET.get("q", None)
        if query:
            qs = qs.filter(
                    Q(title__icontains=query) |
                    Q(creator__username__icontains=query)
                    )

        # URL contains "sort=", sort the list
        sort_by = self.request.GET.get("sort", None)
        if not sort_by or sort_by == "created_time":
            qs = qs.order_by("-created_time")
        elif sort_by == "likes":
            print(sort_by)
            qs = qs.annotate(likes_count=Count('people_liked_this')).order_by("-likes_count")

        # If only needs looking_for_partner
        looking_for_partner = self.request.GET.get("looking_for_partner", None)
        print(looking_for_partner)
        if looking_for_partner == "true":
            qs = qs.filter(looking_for_partner=True)

        # If needs trips that pass a specific place:
        place_id = self.request.GET.get("place_id", None)
        if place_id:
            qs = qs.filter(abstracted_place_list__id=place_id)

        return qs

    def get_serializer_context(self, *args, **kwargs):
        context = super(TripListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context


class TripDetailAPIView(generics.ListAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripModelSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        trip_id = self.kwargs.get("pk")
        qs = Trip.objects.filter(pk=trip_id)
        return qs

class LikeToggleAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk, format=None):
        trip_qs = Trip.objects.filter(pk=pk)
        message = "Not allowed"
        if request.user.is_authenticated():
            is_liked = Trip.objects.like_toggle(request.user, trip_qs.first())
            return Response({'liked': is_liked})
        return Response({"message":message}, status=400)
