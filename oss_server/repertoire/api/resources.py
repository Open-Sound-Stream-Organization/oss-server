from tastypie.resources import ModelResource
from tastypie.authentication import BasicAuthentication
from repertoire.models import Tag, Artist, Album, Playlist, Track


class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = BasicAuthentication(realm="Open Sound Stream: TagResource")

    def obj_create(self, bundle, **kwargs):
        bundle.obj.user = bundle.request.user

class ArtistResource(ModelResource):
    class Meta:
        queryset = Artist.objects.filter()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = BasicAuthentication(realm="Open Sound Stream: ArtistResource")
    def obj_create(self, bundle, **kwargs):
        bundle.obj.user = bundle.request.user

class AlbumResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = BasicAuthentication(realm="Open Sound Stream: AlbumResource")
    def obj_create(self, bundle, **kwargs):
        bundle.obj.user = bundle.request.user

class TrackResource(ModelResource):
    class Meta:
        queryset = Track.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = BasicAuthentication(realm="Open Sound Stream: TrackResource")
    def obj_create(self, bundle, **kwargs):
        bundle.obj.user = bundle.request.user

class PlaylistResource(ModelResource):
    class Meta:
        queryset = Playlist.objects.all()
        allowed_methods = ['get', 'post', 'put', 'delete']
        authentication = BasicAuthentication(realm="Open Sound Stream: PlaylistResource")
    def obj_create(self, bundle, **kwargs):
        bundle.obj.user = bundle.request.user
