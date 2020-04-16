from .resources import *
from tastypie.api import Api

v1_api = Api(api_name="v1")
v1_api.register(TagResource())
v1_api.register(ArtistResource())
v1_api.register(AlbumResource())
v1_api.register(TrackResource())
v1_api.register(PlaylistResource())
v1_api.register(SettingsResource())
v1_api.register(ApiKeyResource())
