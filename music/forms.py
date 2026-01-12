from django import forms
from .models import Artist, Track

class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ["name", "followers"]

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ["name", "release_date", "duration", "artist"]
