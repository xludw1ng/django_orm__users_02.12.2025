from django.urls import path
from .views import (
    ArtistListView,
    ArtistDetailView,
    ArtistCreateView,
    ArtistDeleteView,
    TrackListView,
    TrackDetailView,
    TrackCreateView,
    TrackDeleteView,
)

app_name = "music"

urlpatterns = [
    # Artist
    path("artists/", ArtistListView.as_view(), name="artist-list"),
    path("artists/create/", ArtistCreateView.as_view(), name="artist-create"),
    path("artists/<uuid:artist_id>/", ArtistDetailView.as_view(), name="artist-detail"),
    path("artists/<uuid:artist_id>/delete/", ArtistDeleteView.as_view(), name="artist-delete"),

    # Track
    path("tracks/", TrackListView.as_view(), name="track-list"),
    path("tracks/create/", TrackCreateView.as_view(), name="track-create"),
    path("tracks/<uuid:track_id>/", TrackDetailView.as_view(), name="track-detail"),
    path("tracks/<uuid:track_id>/delete/", TrackDeleteView.as_view(), name="track-delete"),
]
