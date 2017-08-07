from django.conf.urls import url
from django.views.generic.base import RedirectView
from .views import (
    TripListAPIView,
    LikeToggleAPIView,
    TripDetailAPIView,
    )


urlpatterns = [
    url(r'^$', TripListAPIView.as_view(), name='list'),   # /api/trip/
    url(r'^(?P<pk>\d+)/$', TripDetailAPIView.as_view(), name='detail'),     # /api/trip/123321
    url(r'^(?P<pk>\d+)/like/$', LikeToggleAPIView.as_view(), name='like-toggle'),   # /api/trip/123321/like/
]
