from django.contrib import admin
from repertoire.models import Tag, Area, Playlist, Artist, Album, Track, TrackInPlaylist
from repertoire.api.ApiKey import ApiKey
# Register your models here.
admin.site.register(Tag)
admin.site.register(Area)
admin.site.register(Playlist)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(ApiKey)
admin.site.register(TrackInPlaylist)