from django.urls import path
from .views import (
    ArtistListView, ArtistDetailView, ArtistCreateView, ArtistDeleteView,
    TrackListView, TrackDetailView, TrackCreateView, TrackDeleteView,
    ArtistQListView, ArtistBoostFollowersView,
)

app_name = "music"

urlpatterns = [
    path("artists/", ArtistListView.as_view(), name="artist-list"),
    path("artists/create/", ArtistCreateView.as_view(), name="artist-create"),
    path("artists/<uuid:pk>/", ArtistDetailView.as_view(), name="artist-detail"),
    path("artists/<uuid:pk>/delete/", ArtistDeleteView.as_view(), name="artist-delete"),

    path("artists/q/", ArtistQListView.as_view(), name="artist-q"),
    path("artists/boost/", ArtistBoostFollowersView.as_view(), name="artist-boost"),

    path("tracks/", TrackListView.as_view(), name="track-list"),
    path("tracks/create/", TrackCreateView.as_view(), name="track-create"),
    path("tracks/<uuid:pk>/", TrackDetailView.as_view(), name="track-detail"),
    path("tracks/<uuid:pk>/delete/", TrackDeleteView.as_view(), name="track-delete"),
]
