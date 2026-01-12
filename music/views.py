from django.http import JsonResponse, HttpResponseNotAllowed
from django.views import View

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from faker import Faker
from .models import Artist, Track
import random

fake = Faker()



class ArtistListView(View):
    """GET /music/artists/ — список артистов"""

    def get(self, request):
        artists = Artist.objects.all().values('id', 'name', 'followers')
        return JsonResponse(list(artists), safe=False)


class ArtistDetailView(View):
    """GET /music/artists/<uuid:artist_id>/ — один артист"""

    def get(self, request, artist_id):
        try:
            artist = Artist.objects.get(pk=artist_id)
        except Artist.DoesNotExist:
            return JsonResponse({"error": "Artist not found"}, status=404)

        data = {
            "id": str(artist.id),
            "name": artist.name,
            "followers": artist.followers,
        }
        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ArtistCreateView(View):
    """POST /music/artists/create/ — создать артиста с Faker"""

    def post(self, request):
        artist = Artist.objects.create(
            name=fake.name(),
            followers=random.randint(0, 1_000_000),
        )
        return JsonResponse(
            {"created": True, "id": str(artist.id), "name": artist.name},
            status=201
        )

    def get(self, request):
        return HttpResponseNotAllowed(['POST'])



@method_decorator(csrf_exempt, name='dispatch')
class ArtistDeleteView(View):
    """POST /music/artists/<uuid:artist_id>/delete/ — удалить артиста"""

    def post(self, request, artist_id):
        try:
            artist = Artist.objects.get(pk=artist_id)
        except Artist.DoesNotExist:
            return JsonResponse({"error": "Artist not found"}, status=404)

        artist.delete()
        return JsonResponse({"deleted": True})

    def get(self, request, artist_id):
        return HttpResponseNotAllowed(['POST'])

@method_decorator(csrf_exempt, name='dispatch')
class TrackCreateView(View):
    """POST /music/tracks/create/ — создать трек с Faker"""

    def post(self, request):
        # выбираем случайного артиста, если есть
        artist = Artist.objects.order_by('?').first()
        if artist is None:
            artist = Artist.objects.create(
                name=fake.name(),
                followers=random.randint(0, 1_000_000),
            )

        track = Track.objects.create(
            name=fake.sentence(nb_words=3),
            release_date=fake.date_between(start_date='-5y', end_date='today'),
            duration=random.uniform(120, 420),
            artist=artist,
        )
        return JsonResponse(
            {
                "created": True,
                "id": str(track.id),
                "name": track.name,
                "artist": artist.name,
            },
            status=201
        )

    def get(self, request):
        return HttpResponseNotAllowed(['POST'])


class TrackListView(View):
    """GET /music/tracks/ — список треков"""

    def get(self, request):
        tracks = Track.objects.all().values(
            'id', 'name', 'release_date', 'duration', 'artist__name'
        )
        # переименуем ключ artist__name → artist
        result = []
        for t in tracks:
            result.append({
                "id": str(t["id"]),
                "name": t["name"],
                "release_date": t["release_date"],
                "duration": t["duration"],
                "artist": t["artist__name"],
            })
        return JsonResponse(result, safe=False)


class TrackDetailView(View):
    """GET /music/tracks/<uuid:track_id>/ — один трек"""

    def get(self, request, track_id):
        try:
            track = Track.objects.select_related('artist').get(pk=track_id)
        except Track.DoesNotExist:
            return JsonResponse({"error": "Track not found"}, status=404)

        data = {
            "id": str(track.id),
            "name": track.name,
            "release_date": track.release_date,
            "duration": track.duration,
            "artist": track.artist.name,
        }
        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class TrackDeleteView(View):
    """POST /music/tracks/<uuid:track_id>/delete/ — удалить трек"""

    def post(self, request, track_id):
        try:
            track = Track.objects.get(pk=track_id)
        except Track.DoesNotExist:
            return JsonResponse({"error": "Track not found"}, status=404)

        track.delete()
        return JsonResponse({"deleted": True})

    def get(self, request, track_id):
        return HttpResponseNotAllowed(['POST'])

