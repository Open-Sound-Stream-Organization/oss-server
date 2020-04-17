from django.contrib.auth.models import User
from django.db.models import Model, CharField, TextField, ForeignKey, ManyToManyField, CASCADE, PROTECT, IntegerField, DateField, ImageField, FileField
from django.db.models import Q

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
        ("O", "Other"),
    ]
    type = CharField(max_length=1, choices=formation_types, verbose_name='Type of Artist (Person/Group/etc.)')
    area = ForeignKey(Area, on_delete=PROTECT, blank=True, null=True, verbose_name='Area of Artist')
    begin = DateField("Date of persons birth/Date of group formation", blank=True, null=True)
    end = DateField("Death of person/Group dissolved - blank if still together", blank=True, null=True)
    user = ForeignKey(User, on_delete=CASCADE)
    tags = ManyToManyField(Tag, verbose_name='Tags', blank=True)
    
    def __str__(self):
        return "{}; '{}'".format(self.user.username, self.name)
    


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
    album = ForeignKey(Album, on_delete=CASCADE, verbose_name='Track in Album')
    user = ForeignKey(User, on_delete=CASCADE)
    artist = ManyToManyField(Artist, verbose_name='From Artist')
    tags = ManyToManyField(Tag, blank=True)
    audio = FileField(upload_to=audio_path, blank=True,
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