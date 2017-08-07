from django.conf.urls import url
from django.views.generic.base import RedirectView
from .views import (
    PlaceListAPIView,
    )


urlpatterns = [
    url(r'^$', PlaceListAPIView.as_view(), name='list'),   # /api/place/
    # url(r'^(?P<pk>\d+)/$', TripDetailAPIView.as_view(), name='detail'),     # /api/place/123321
]
