from django.contrib import admin

from .models import Place, PlaceDetailInATrip
# Register your models here.
class PlaceDetailInATripInline(admin.TabularInline):
    model = PlaceDetailInATrip

class PlaceAdmin(admin.ModelAdmin):
    inlines = (PlaceDetailInATripInline,)

admin.site.register(Place, PlaceAdmin)
