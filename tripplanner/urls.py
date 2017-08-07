"""tripplanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

from accounts.views import UserRegisterView
from .views import home

urlpatterns = [
    url(r'^antiflee/', admin.site.urls),
    url(r'^$', home, name='home'),
    url(r'^register/$', UserRegisterView.as_view(), name='register'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^profiles/', include('accounts.urls', namespace='profiles')),
    url(r'^api/trip/', include('trips.api.urls', namespace='trip-api')),
    url(r'^api/place/', include('places.api.urls', namespace='place-api')),
    url(r'^api/', include('accounts.api.urls', namespace='profiles-api')),
    url(r'^trip/', include('trips.urls', namespace='trip')),
    url(r'^place/', include('places.urls', namespace='place')),
]

if settings.DEBUG:
    urlpatterns += (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
    urlpatterns += (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
