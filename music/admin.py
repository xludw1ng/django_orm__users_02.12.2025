from django.contrib import admin
from .models import Artist, Track


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'followers', 'created_at')
    search_fields = ('name',)
    list_editable = ('followers',)


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'release_date', 'duration')
    search_fields = ('name', 'artist__name')
    list_filter = ('artist', 'release_date')
