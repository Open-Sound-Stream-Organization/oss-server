from tastypie.authentication import BasicAuthentication, MultiAuthentication
from tastypie.fields import ToOneField, ToManyField
from tastypie.resources import ModelResource

from repertoire.api.ApiKey import ApiKey
from repertoire.api.ApiKeyOnlyAuthentication import ApiKeyOnlyAuthentication
from repertoire.api.authorization import UserObjectsOnlyAuthorization
from repertoire.models import Tag, Artist, Album, Playlist, Track, Settings


class TagResource(ModelResource):
    artists = ToManyField('repertoire.api.resources.ArtistResource',
                          attribute=lambda bundle: Artist.objects.filter(tags=bundle.obj, user=bundle.obj.user),
                          related_name='artist', blank=True, null=True)
    albums = ToManyField('repertoire.api.resources.AlbumResource',
                         attribute=lambda bundle: Artist.objects.filter(tags=bundle.obj, user=bundle.obj.user),
                         blank=True, null=True)
    tracks = ToManyField('repertoire.api.resources.TrackResource',
                         attribute=lambda bundle: Track.objects.filter(tags=bundle.obj, user=bundle.obj.user),
                         blank=True, null=True)
    playlists = ToManyField('repertoire.api.resources.PlaylistResource',
                            attribute=lambda bundle: Playlist.objects.filter(tags=bundle.obj, user=bundle.obj.user),
                            blank=True, null=True)

    class Meta:
        queryset = Tag.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = MultiAuthentication(BasicAuthentication(realm="Open Sound Stream: TagResource"),
                                             ApiKeyOnlyAuthentication())
        authorization = UserObjectsOnlyAuthorization()

    def obj_create(self, bundle, **kwargs):
        return super(TagResource, self).obj_create(bundle, user=bundle.request.user)


class ArtistResource(ModelResource):
    tags = ToManyField(TagResource, attribute=lambda bundle: Tag.objects.filter(artist=bundle.obj), blank=True)
    albums = ToManyField("repertoire.api.resources.AlbumResource",
                         attribute=lambda bundle: Album.objects.filter(artist=bundle.obj), blank=True, null=True)
    tracks = ToManyField("repertoire.api.resources.TrackResource",
                         attribute=lambda bundle: Track.objects.filter(artist=bundle.obj), blank=True, null=True)

    class Meta:
        queryset = Artist.objects.filter()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = MultiAuthentication(BasicAuthentication(realm="Open Sound Stream: ArtistResource"),
                                             ApiKeyOnlyAuthentication())
        authorization = UserObjectsOnlyAuthorization()

    def obj_create(self, bundle, **kwargs):
        return super(ArtistResource, self).obj_create(bundle, user=bundle.request.user)


class AlbumResource(ModelResource):
    tags = ToManyField(TagResource, attribute=lambda bundle: Tag.objects.filter(album=bundle.obj), blank=True,
                       null=True)
    artists = ToManyField("repertoire.api.resources.ArtistResource",
                          attribute=lambda bundle: Artist.objects.filter(album=bundle.obj), blank=True, null=True)
    tracks = ToManyField("repertoire.api.resources.TrackResource",
                         attribute=lambda bundle: Track.objects.filter(album=bundle.obj), blank=True, null=True)

    class Meta:
        queryset = Album.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = MultiAuthentication(BasicAuthentication(realm="Open Sound Stream: AlbumResource"),
                                             ApiKeyOnlyAuthentication())
        authorization = UserObjectsOnlyAuthorization()

    def obj_create(self, bundle, **kwargs):
        return super(AlbumResource, self).obj_create(bundle, user=bundle.request.user)


class TrackResource(ModelResource):
    tags = ToManyField(TagResource, attribute=lambda bundle: Tag.objects.filter(track=bundle.obj), blank=True,
                       null=True, )
    album = ToOneField("repertoire.api.resources.AlbumResource",
                       attribute=lambda bundle: Album.objects.filter(track=bundle.obj).first(), blank=True, null=True)
    artists = ToManyField("repertoire.api.resources.ArtistResource",
                          attribute=lambda bundle: Artist.objects.filter(track=bundle.obj), blank=True, null=True)

    class Meta:
        queryset = Track.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = MultiAuthentication(BasicAuthentication(realm="Open Sound Stream: TrackResource"),
                                             ApiKeyOnlyAuthentication())
        authorization = UserObjectsOnlyAuthorization()

    def obj_create(self, bundle, **kwargs):
        return super(TrackResource, self).obj_create(bundle, user=bundle.request.user)

    def dehydrate(self, bundle):
        bundle.data['audio'] = "repertoire/track_file/{}/".format(bundle.data['id'])
        return bundle


class PlaylistResource(ModelResource):
    tags = ToManyField(TagResource, attribute=lambda bundle: Tag.objects.filter(playlist=bundle.obj), blank=True,
                       null=True, full=True, full_detail=True, full_list=False)

    class Meta:
        queryset = Playlist.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = MultiAuthentication(BasicAuthentication(realm="Open Sound Stream: PlaylistResource"),
                                             ApiKeyOnlyAuthentication())
        authorization = UserObjectsOnlyAuthorization()

    def obj_create(self, bundle, **kwargs):
        return super(PlaylistResource, self).obj_create(bundle, user=bundle.request.user)


class ApiKeyResource(ModelResource):
    class Meta:
        queryset = ApiKey.objects.all()
        allowed_methods = ['get', 'post', 'delete']
        always_return_data = True
        authentication = BasicAuthentication(realm="Open Sound Stream: ApiKeyResource")
        authorization = UserObjectsOnlyAuthorization()
        excludes = ['key', 'shown']

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

    def obj_create(self, bundle, **kwargs):
        return super(ApiKeyResource, self).obj_create(bundle, user=bundle.request.user)
