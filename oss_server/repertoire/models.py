import musicbrainzngs
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model, CharField, TextField, ForeignKey, ManyToManyField, CASCADE, PROTECT, IntegerField, \
    DateField, ImageField, FileField

from dateutil.parser import parse


class Tag(Model):
    name = CharField(max_length=1024, verbose_name='Tag name')
    user = ForeignKey(User, on_delete=CASCADE, verbose_name='Tag belongs to User')
    
    def __str__(self):
        return "{}; '{}'".format(self.user.username, self.name)


class Area(Model):
    name = CharField(max_length=512, verbose_name='Area Name')
    mbid = CharField(max_length=64, verbose_name='Musicbrainz ID')
    area_categories = [
        ("X", "Country"),
        ("L", "Subdivision"),
        ("C", "County"),
        ("M", "Municipality"),
        ("S", "City"),
        ("D", "District"),
        ("I", "Island"),
    ]
    type = CharField(max_length=2, choices=area_categories, verbose_name='Area Type')
    country_code = CharField(max_length=2, verbose_name='iso-3166-1-code', blank=True, null=True)
    user = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return self.name


class Artist(Model):
    name = CharField(max_length=512, verbose_name='Name of Artist')
    mbid = CharField(max_length=64, blank=True, verbose_name='Musicbrainz ID')
    formation_types = [
        ("P", "Person"),
        ("G", "Group"),
        ("O", "Orchestra"),
        ("C", "Choir"),
        ("F", "Character"),
        ("E", "Other"),
    ]
    type = CharField(max_length=1, choices=formation_types, verbose_name='Type of Artist (Person/Group/etc.)')
    area = ForeignKey(Area, on_delete=PROTECT, blank=True, null=True, verbose_name='Area of Artist')
    begin = DateField("Date of persons birth/Date of group formation", blank=True, null=True)
    end = DateField("Death of person/Group dissolved - blank if still together", blank=True, null=True)
    user = ForeignKey(User, on_delete=CASCADE)
    tags = ManyToManyField(Tag, verbose_name='Tags', blank=True)
    
    def __str__(self):
        return "{}; '{}'".format(self.user.username, self.name)

    @staticmethod
    def new_artist_by_mbid(user: User, mbid: str) -> 'Artist':
        """
        Creates a new Artist based on the MusicBrainz.org identifier
        :param user: the user associated with the query
        :param mbid: Musicbrainz.org identifier
        :param artist_name: Optional hint for artist name, if specified no query will be executed
        :return: newly created artist
        """
        musicbrainzngs.set_useragent('Open_Sound_Stream:Server', settings.OSS_VERSION)
        try:
            mbdata = musicbrainzngs.get_artist_by_id(mbid)
        except musicbrainzngs.WebServiceError:
            raise ConnectionError("The MusicBrainz Database could not be reached")
        else:
            artist = mbdata["artist"]
            artistobj: Artist
            artistobj, created = Artist.objects.get_or_create(user=user, name=artist["name"])
            artistobj.mbid = mbid
            for letter, formation in Artist.formation_types:
                if formation == artist['type']:
                    artistobj.type = letter
                    break
                else:
                    artistobj.type = 'E' #other type
            if 'life-span' in artist:
                lifespan = artist['life-span']
                if 'begin' in lifespan:
                    artistobj.begin = parse(lifespan['begin']).date().isoformat()
                if 'end' in lifespan:
                    artistobj.end = parse(lifespan['end']).date().isoformat()
            artistobj.save()
            return artistobj

    @staticmethod
    def get_by_mbid( user: User, mbid: str, artist_name: str=None):
        try:
            return Artist.objects.get(user=user, mbid=mbid)
        except ObjectDoesNotExist:
            try:
                return Artist.new_artist_by_mbid(user, mbid)
            except ConnectionError:
                return None


class Album(Model):
    name = TextField(verbose_name='Album Name')
    mbid = CharField(max_length=64, blank=True, null=True, verbose_name='Musicbrainz ID')
    release = DateField(blank=True, null=True, verbose_name='First release of Album')
    artist = ManyToManyField(Artist, verbose_name='Album Artist(s)')
    cover_url = CharField(max_length=1024, blank=True, null=True, verbose_name='Url of Cover-Image')
    cover_file = ImageField(blank=True, null=True, verbose_name='Custom Cover-Image')
    user = ForeignKey(User, on_delete=CASCADE)
    tags = ManyToManyField(Tag, blank=True)

    def get_cover(self):
        if self.cover_file:
            return self.cover_file.url
        else:
            return self.cover_url
    
    def __str__(self):
        return "{}; '{}'".format(self.user.username, self.name)


def audio_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Track(Model):
    title = CharField(max_length=512, verbose_name='Track Title')
    mbid = CharField(max_length=64, blank=True, null=True, verbose_name='Musicbrainz ID')
    album = ForeignKey(Album, on_delete=CASCADE, verbose_name='Track in Album', blank=True, null=True)
    user = ForeignKey(User, on_delete=CASCADE)
    artist = ManyToManyField(Artist, verbose_name='From Artist', blank=True)
    tags = ManyToManyField(Tag, blank=True)
    audio = FileField(upload_to=audio_path, blank=True, null=True,
                       help_text=("Allowed type - .mp3, .wav, .ogg"), verbose_name='Audio File')
    def __str__(self):
        return "{}; '{}'".format(self.user.username, self.title)


class Playlist(Model):
    name = CharField(max_length=512, verbose_name='Name of Playlist')
    tracks = ManyToManyField(Track, through='TrackInPlaylist', verbose_name='Tracks in Playlist')
    tags = ManyToManyField(Tag, blank=True)
    user = ForeignKey(User, on_delete=CASCADE)
    
    def __str__(self):
        return "{}; '{}'".format(self.user.username, self.name)


class TrackInPlaylist(Model):
    playlist = ForeignKey(Playlist, on_delete=CASCADE)
    track = ForeignKey(Track, on_delete=CASCADE)
    sort_number = IntegerField(verbose_name='Arbitrary Sort Number')
    
    def __str__(self):
        return "{}; Track '{}' in Playlist '{}'".format(self.playlist.user.username, self.track.title, self.playlist.name)

class Settings(Model):
    '''Holds settings for syncing across devices'''
    identifier = CharField(max_length=128, verbose_name='Setting Identifier')
    data = TextField(verbose_name='Data holding identifier')
    user = ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return "{}: Setting: {}".format(self.user, self.identifier)