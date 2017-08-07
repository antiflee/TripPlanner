from django.conf.urls import url
from .views import (
            TripListView,
            TripDetailView,
            TripCreateView,
            TripUpdateView,
            tripDelete,
            # tripCreate,
            # tripDetail,
            )


urlpatterns = [
    url(r'^$', TripListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', TripDetailView.as_view(), name='detail'),
    # url(r'^(?P<pk>\d+)/$', tripDetail, name='detail'),
    url(r'^create/$', TripCreateView.as_view(), name='create'),
    # url(r'^create/$', tripCreate, name='create'),
    url(r'^(?P<pk>\d+)/update/$', TripUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', tripDelete, name='delete'),
]
