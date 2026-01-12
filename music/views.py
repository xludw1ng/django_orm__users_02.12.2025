from django.views import View
from django.db.models import F, Q
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .models import Artist, Track
from .forms import ArtistForm, TrackForm


class ArtistListView(ListView):
    model = Artist
    template_name = "music/artist_list.html"
    context_object_name = "artists"

    def get_queryset(self):
        qs = Artist.objects.all()

        name = self.request.GET.get("name")
        if name:
            qs = qs.filter(name__icontains=name)

        sort = self.request.GET.get("sort")
        allowed = {"name", "-name", "followers", "-followers"}
        if sort in allowed:
            qs = qs.order_by(sort)

        return qs


class ArtistCreateView(CreateView):
    model = Artist
    form_class = ArtistForm
    template_name = "music/artist_form.html"
    success_url = reverse_lazy("music:artist-list")


class ArtistDetailView(DetailView):
    model = Artist
    template_name = "music/artist_detail.html"
    context_object_name = "artist"


class ArtistDeleteView(DeleteView):
    model = Artist
    template_name = "music/artist_confirm_delete.html"
    success_url = reverse_lazy("music:artist-list")


class TrackListView(ListView):
    model = Track
    template_name = "music/track_list.html"
    context_object_name = "tracks"

    def get_queryset(self):
        return Track.objects.select_related("artist").all()


class TrackCreateView(CreateView):
    model = Track
    form_class = TrackForm
    template_name = "music/track_form.html"
    success_url = reverse_lazy("music:track-list")


class TrackDetailView(DetailView):
    model = Track
    template_name = "music/track_detail.html"
    context_object_name = "track"


class TrackDeleteView(DeleteView):
    model = Track
    template_name = "music/track_confirm_delete.html"
    success_url = reverse_lazy("music:track-list")


class ArtistQListView(ListView):
    model = Artist
    template_name = "music/artist_q_list.html"
    context_object_name = "artists"

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        min_f = self.request.GET.get("min", "")

        cond = Q()
        if q:
            cond |= Q(name__icontains=q)
        if min_f:
            cond |= Q(followers__gte=int(min_f))

        return Artist.objects.filter(cond) if cond else Artist.objects.all()


class ArtistBoostFollowersView(View):
    def post(self, request):
        Artist.objects.filter(followers__lt=500000).update(followers=F("followers") + 1000)
        return redirect("music:artist-list")
