from django.contrib import admin

# from .forms import TripModelForm
from .models import Trip, PlaceVisited, TravelMode
# Register your models here.

class PlaceVisitedInline(admin.TabularInline):
    model = PlaceVisited

class TripAdmin(admin.ModelAdmin):
    # form = TripModelForm
    inlines = (PlaceVisitedInline,)

    # class Meta:
    #     model = Trip

admin.site.register(Trip, TripAdmin)
admin.site.register(PlaceVisited)
admin.site.register(TravelMode)
