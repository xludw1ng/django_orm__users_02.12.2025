from django.views import View
from django.db.models import F, Q
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .models import Artist, Track
from .forms import ArtistForm, TrackForm
from django.contrib.auth.mixins import LoginRequiredMixin


class ArtistListView(LoginRequiredMixin, ListView):
    model = Artist
    template_name = "music/artist_list.html"
    context_object_name = "artists"

    def get_queryset(self):
        qs = Artist.objects.filter(owner=self.request.user)

        name = self.request.GET.get("name")
        if name:
            qs = qs.filter(name__icontains=name)

        sort = self.request.GET.get("sort")
        allowed = {"name", "-name", "followers", "-followers"}
        if sort in allowed:
            qs = qs.order_by(sort)

        return qs


class ArtistCreateView(LoginRequiredMixin, CreateView):
    model = Artist
    form_class = ArtistForm
    template_name = "music/artist_form.html"
    success_url = reverse_lazy("music:artist-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ArtistDetailView(LoginRequiredMixin, DetailView):
    model = Artist
    template_name = "music/artist_detail.html"
    context_object_name = "artist"

    def get_queryset(self):
        return Artist.objects.filter(owner=self.request.user)


class ArtistDeleteView(LoginRequiredMixin, DeleteView):
    model = Artist
    template_name = "music/artist_confirm_delete.html"
    success_url = reverse_lazy("music:artist-list")

    def get_queryset(self):
        return Artist.objects.filter(owner=self.request.user)


class TrackListView(LoginRequiredMixin, ListView):
    model = Track
    template_name = "music/track_list.html"
    context_object_name = "tracks"

    def get_queryset(self):
        return Track.objects.select_related("artist").filter(owner=self.request.user)


class TrackCreateView(LoginRequiredMixin, CreateView):
    model = Track
    form_class = TrackForm
    template_name = "music/track_form.html"
    success_url = reverse_lazy("music:track-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["artist"].queryset = Artist.objects.filter(owner=self.request.user)
        return form


class TrackDetailView(LoginRequiredMixin, DetailView):
    model = Track
    template_name = "music/track_detail.html"
    context_object_name = "track"

    def get_queryset(self):
        return Track.objects.select_related("artist").filter(owner=self.request.user)


class TrackDeleteView(LoginRequiredMixin, DeleteView):
    model = Track
    template_name = "music/track_confirm_delete.html"
    success_url = reverse_lazy("music:track-list")

    def get_queryset(self):
        return Track.objects.filter(owner=self.request.user)


class ArtistQListView(LoginRequiredMixin, ListView):
    model = Artist
    template_name = "music/artist_q_list.html"
    context_object_name = "artists"

    def get_queryset(self):
        q = (self.request.GET.get("q") or "").strip()
        min_f = (self.request.GET.get("min") or "").strip()

        qs = Artist.objects.filter(owner=self.request.user)

        or_part = Q()
        if q:
            or_part |= Q(name__icontains=q)
        if min_f.isdigit():
            or_part |= Q(followers__gte=int(min_f))

        if q or min_f:
            qs = qs.filter(or_part)

        return qs


class ArtistBoostFollowersView(LoginRequiredMixin, View):
    def post(self, request):
        Artist.objects.filter(owner=request.user, followers__lt=500000).update(
            followers=F("followers") + 1000
        )
        return redirect("music:artist-list")

