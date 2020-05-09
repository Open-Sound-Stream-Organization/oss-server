from typing import Dict, List, Union

import musicbrainzngs
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from tastypie.authentication import BasicAuthentication, MultiAuthentication
from tastypie.fields import ToOneField, ToManyField, FileField
from tastypie.resources import ModelResource

from mutagen import File as GetTags

from repertoire.api.ApiKey import ApiKey
from repertoire.api.MultipartUploadMixin import MultipartResourceMixin
from repertoire.api.ApiKeyOnlyAuthentication import ApiKeyOnlyAuthentication, ApiKeyOnlyOnSelfDelete
from repertoire.api.authorization import UserObjectsOnlyAuthorization
from repertoire.models import Tag, Artist, Album, Playlist, Track, Settings, Area, TrackInPlaylist

from django.conf import settings
import acoustid


class AreaResource(ModelResource):
    artists = ToManyField('repertoire.api.resources.ArtistResource', 'artist_set', related_name='artist', blank=True,
                          null=True)

    class Meta:
        queryset = Area.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = MultiAuthentication(BasicAuthentication(realm="Open Sound Stream: TagResource"),
                                             ApiKeyOnlyAuthentication())
        authorization = UserObjectsOnlyAuthorization()
        always_return_data = True
        excludes = ['user']

    def obj_create(self, bundle, **kwargs):
        return super(AreaResource, self).obj_create(bundle, user=bundle.request.user)


class TagResource(ModelResource):
    artists = ToManyField('repertoire.api.resources.ArtistResource', 'artist_set', blank=True, null=True)
    albums = ToManyField('repertoire.api.resources.AlbumResource', 'album_set', blank=True, null=True)
    songs = ToManyField('repertoire.api.resources.SongResource', 'track_set', blank=True, null=True)
    playlists = ToManyField('repertoire.api.resources.PlaylistResource', 'playlist_set', blank=True, null=True)

    class Meta:
        queryset = Tag.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = MultiAuthentication(BasicAuthentication(realm="Open Sound Stream: TagResource"),
                                             ApiKeyOnlyAuthentication())
        authorization = UserObjectsOnlyAuthorization()
        always_return_data = True
        excludes = ['user']

    def obj_create(self, bundle, **kwargs):
        return super(TagResource, self).obj_create(bundle, user=bundle.request.user)


class ArtistResource(ModelResource):
    tags = ToManyField(TagResource, 'tags', blank=True)
    albums = ToManyField("repertoire.api.resources.AlbumResource", 'album_set', blank=True, null=True)
    songs = ToManyField("repertoire.api.resources.SongResource", 'track_set', blank=True, null=True)

    class Meta:
        queryset = Artist.objects.filter()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = MultiAuthentication(BasicAuthentication(realm="Open Sound Stream: ArtistResource"),
                                             ApiKeyOnlyAuthentication())
        authorization = UserObjectsOnlyAuthorization()
        always_return_data = True
        excludes = ['user']

    def obj_create(self, bundle, **kwargs):
        return super(ArtistResource, self).obj_create(bundle, user=bundle.request.user)


class AlbumResource(ModelResource):
    tags = ToManyField(TagResource, 'tags', blank=True, null=True)
    artists = ToManyField("repertoire.api.resources.ArtistResource", 'artist', blank=True, null=True)
    songs = ToManyField("repertoire.api.resources.SongResource", 'track_set', blank=True, null=True)

    class Meta:
        queryset = Album.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = MultiAuthentication(BasicAuthentication(realm="Open Sound Stream: AlbumResource"),
                                             ApiKeyOnlyAuthentication())
        authorization = UserObjectsOnlyAuthorization()
        always_return_data = True
        excludes = ['user']

    def obj_create(self, bundle, **kwargs):
        return super(AlbumResource, self).obj_create(bundle, user=bundle.request.user)


class TrackResource(MultipartResourceMixin, ModelResource):
    tags = ToManyField(TagResource, 'tags', blank=True, null=True)
    album = ToOneField("repertoire.api.resources.AlbumResource", 'album', blank=True, null=True)
    artists = ToManyField("repertoire.api.resources.ArtistResource", 'artist', blank=True, null=True)

    class Meta:
        queryset = Track.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = MultiAuthentication(BasicAuthentication(realm="Open Sound Stream: TrackResource"),
                                             ApiKeyOnlyAuthentication())
        authorization = UserObjectsOnlyAuthorization()
        always_return_data = True
        excludes = ['user']

    def obj_create(self, bundle, **kwargs):
        return super(TrackResource, self).obj_create(bundle, user=bundle.request.user)

    def dehydrate(self, bundle):
        bundle.data['audio'] = "repertoire/song_file/{}/".format(bundle.data['id'])
        return bundle

    def hydrate(self, bundle):
        #Translate model field name to audio metadata name
        tag_name_translator: Dict[str, List[str]] = {
            'title': ['title'],
        }
        if 'audio' in bundle.data.keys():
            if settings.USE_ACOUSTID:
                tmp_file_path = bundle.data.get('audio').temporary_file_path()
                matches = acoustid.match(settings.ACOUSTID_API_KEY, tmp_file_path)
                try:
                    score, recording_id, title, artist_entry = next(matches)
                except StopIteration:
                    pass
                else:
                    musicbrainzngs.set_useragent('Open_Sound_Stream:Server', settings.OSS_VERSION)
                    try:
                        rec = musicbrainzngs.get_recording_by_id(recording_id, includes=['artists', 'tags', 'releases'])
                    except musicbrainzngs.WebServiceError:
                        pass
                    else:
                        bundle_data_translate: Dict[str, Union[List[str], List[Artist], List[Album]]] = {
                            'title': title,
                            'mbid': recording_id,
                        }
                        for key, val in bundle_data_translate.items():
                            if key not in bundle.data:
                                bundle.data[key] = val
                        artists: List[str] = []
                        artist_obj_list: List[Artist] = []
                        if "artists" not in bundle.data:
                            artist_list: List[Dict] = rec['recording']['artist-credit']
                            for artist_entry in artist_list:
                                artist_by_id: Artist = Artist.get_by_mbid(bundle.obj.user, artist_entry["artist"]["id"])
                                if artist_by_id is not None:
                                    artists.append("/api/v1/artist/{}/".format(artist_by_id.pk))
                                    artist_obj_list.append(artist_by_id)
                            bundle.data['artists'] = artists
                        else:
                            for artist_entry in bundle.data.getlist('artist'):
                                artist_entry_splitted = artist_entry.split("/")
                                if artist_entry_splitted[-1] == '':
                                    del artist_entry_splitted[-1]
                                try:
                                    artist_id = int(artist_entry_splitted[-1])
                                except ValueError:
                                    continue
                                try:
                                    artist_obj_list.append(Artist.objects.get(user=bundle.obj.user, pk=artist_id))
                                except ObjectDoesNotExist:
                                    #dont process any further, let tastypie throw the exception
                                    return bundle
                        if "album" not in bundle.data and len(rec['recording']['release-list']) >= 1:
                            release = rec['recording']['release-list'][0]
                            album, created = Album.objects.get_or_create(user=bundle.obj.user, name=release['title'])
                            for artist_entry in artist_obj_list:
                                album.artist.add(artist_entry)
                            album.save()
                            bundle.data['album'] = "/api/v1/album/{}/".format(album.pk)
            metadata = GetTags(fileobj=bundle.data['audio'].file)
            for field_name, tag_names in tag_name_translator.items():
                if field_name not in bundle.data.keys():
                    for tag_name in tag_names:
                        if tag_name in metadata.keys():
                            bundle.data[field_name] = metadata.get(tag_name)
                            break
        return bundle


class SongResource(TrackResource):
    audio = FileField(attribute='audio', blank=True, null=True)
    playlists = ToManyField("repertoire.api.resources.PlaylistResource", 'playlist_set', full=False, blank=True, null=True)

    class Meta:
        resource_name = 'song'
        queryset = Track.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = MultiAuthentication(BasicAuthentication(realm="Open Sound Stream: SongResource"),
                                             ApiKeyOnlyAuthentication())
        authorization = UserObjectsOnlyAuthorization()
        always_return_data = True
        excludes = ['user']


class SongInPlaylistResource(ModelResource):
    playlist = ToOneField("repertoire.api.resources.PlaylistResource", 'playlist', full=False)
    song = ToOneField(SongResource, 'track', full=True, full_detail=True, full_list=True)
    class Meta:
        queryset = TrackInPlaylist.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = MultiAuthentication(BasicAuthentication(realm="Open Sound Stream: SongResource"),
                                             ApiKeyOnlyAuthentication())
        authorization = UserObjectsOnlyAuthorization()
        always_return_data = True
        excludes = ['user']


class PlaylistResource(ModelResource):
    tags = ToManyField(TagResource, attribute=lambda bundle: Tag.objects.filter(playlist=bundle.obj), blank=True,
                       null=True, full=True, full_detail=True, full_list=False)
    songsinplaylist = ToManyField(SongInPlaylistResource, 'trackinplaylist_set', blank=True, null=True, full=True,
                                  full_detail=True, full_list=True)

    class Meta:
        queryset = Playlist.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = MultiAuthentication(BasicAuthentication(realm="Open Sound Stream: PlaylistResource"),
                                             ApiKeyOnlyAuthentication())
        authorization = UserObjectsOnlyAuthorization()
        always_return_data = True
        excludes = ['user']

    def obj_create(self, bundle, **kwargs):
        return super(PlaylistResource, self).obj_create(bundle, user=bundle.request.user)


class ApiKeyResource(ModelResource):
    class Meta:
        queryset = ApiKey.objects.all()
        allowed_methods = ['get', 'post', 'delete']
        always_return_data = True
        authentication = MultiAuthentication(
                            BasicAuthentication(realm="Open Sound Stream: ApiKeyResource"),
                            ApiKeyOnlyOnSelfDelete())
        authorization = UserObjectsOnlyAuthorization()
        excludes = ['key', 'shown', 'user']

    def dehydrate(self, bundle):
        if bundle.request.method == 'POST' and not bundle.obj.shown:
            bundle.data['key'] = bundle.obj.key
            bundle.obj.shown = True
            bundle.obj.save()
        return bundle

    def obj_create(self, bundle, **kwargs):
        return super(ApiKeyResource, self).obj_create(bundle, user=bundle.request.user)


class SettingsResource(ModelResource):
    class Meta:
        queryset = Settings.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = MultiAuthentication(BasicAuthentication(realm="Open Sound Stream: PlaylistResource"),
                                             ApiKeyOnlyAuthentication())
        authorization = UserObjectsOnlyAuthorization()
        always_return_data = True
        excludes = ['user']

    def obj_create(self, bundle, **kwargs):
        return super(SettingsResource, self).obj_create(bundle, user=bundle.request.user)
