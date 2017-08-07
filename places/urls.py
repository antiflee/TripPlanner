from django.conf.urls import url
from .views import (
            PlaceListView,
            PlaceDetailView,
            PlaceHeatmapView,
            )


urlpatterns = [
    url(r'^$', PlaceListView.as_view(), name='list'),
    url(r'^heatmap/$', PlaceHeatmapView.as_view(), name='heatmap'),
    url(r'^(?P<pk>\d+)/$', PlaceDetailView.as_view(), name='detail'),
]
