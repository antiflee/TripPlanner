from django.conf.urls import url
from django.views.generic.base import RedirectView
from trips.api.views import (
    TripListAPIView
    )


urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/trip/$', TripListAPIView.as_view(), name='list'),
]
