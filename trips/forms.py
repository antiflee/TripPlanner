from django import forms

from .models import Trip, PlaceVisited

class TripModelForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = [
            "title",
        ]

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get("title")
        if title == "abc":
            raise forms.ValidationError("Cannot be ABC")
        return title

class PlaceVisitedForm(forms.ModelForm):
    class Meta:
        model = PlaceVisited
        fields = [
            'travel_mode_to_here',
        ]
