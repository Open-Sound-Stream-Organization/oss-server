from django.contrib.auth.models import User
from django.db.models import Model, CharField, TextField, ForeignKey, ManyToManyField, CASCADE, PROTECT, IntegerField, DateField, ImageField, FileField

class Tag(Model):
    name = CharField(max_length=1024)
    user = ForeignKey(User, on_delete=CASCADE)
    
    def __str__(self):
        return "{}; '{}'".format(self.user.username, self.name)


class Area(Model):
    name = CharField(max_length=512)
    mbid = CharField(max_length=64)
    area_categories = [
        ("X", "Country"),
        ("L", "Subdivision"),
        ("C", "County"),
        ("M", "Municipality"),
        ("S", "City"),
        ("D", "District"),
        ("I", "Island"),
    ]
    type = CharField(max_length=2, choices=area_categories)
    country_code = CharField(max_length=2, verbose_name='iso-3166-1-code', blank=True, null=True)
    
    def __str__(self):
        return self.name

class Artist(Model):
    name = CharField(max_length=512)
    mbid = CharField(max_length=64, blank=True)
    formation_types = [
        ("P", "Person"),
        ("G", "Group"),
        ("O", "Orchestra"),
        ("C", "Choir"),
        ("F", "Character"),
        ("O", "Other"),
    ]
    type = CharField(max_length=1, choices=formation_types)
    area = ForeignKey(Area, on_delete=PROTECT, blank=True, null=True)
    begin = DateField("Date of persons birth/Date of group formation", blank=True, null=True)
    end = DateField("Death of person/Group dissolved - blank if still together", blank=True, null=True)
    user = ForeignKey(User, on_delete=CASCADE)
    tags = ManyToManyField(Tag)
    
    def __str__(self):
        return "{}; '{}'".format(self.user.username, self.name)
    


class Album(Model):
    name = TextField()
    mbid = CharField(max_length=64, blank=True, null=True)
    release = DateField(blank=True)
    artist = ManyToManyField(Artist)
    cover_url = CharField(max_length=1024, blank=True, null=True)
    cover_file = ImageField(blank=True, null=True)
    user = ForeignKey(User, on_delete=CASCADE)
    tags = ManyToManyField(Tag)

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
    title = CharField(max_length=512)
    mbid = CharField(max_length=64, blank=True, null=True)
    album = ForeignKey(Album, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    artist = ManyToManyField(Artist)
    tags = ManyToManyField(Tag)
    audio = FileField(upload_to=audio_path, blank=True,
                       help_text=("Allowed type - .mp3, .wav, .ogg"))
    def __str__(self):
        return "{}; '{}'".format(self.user.username, self.title)


class Playlist(Model):
    name = CharField(max_length=512)
    tracks = ManyToManyField(Track, through='TrackInPlaylist')
    tags = ManyToManyField(Tag)
    user = ForeignKey(User, on_delete=CASCADE)
    
    def __str__(self):
        return "{}; '{}'".format(self.user.username, self.name)


class TrackInPlaylist(Model):
    playlist = ForeignKey(Playlist, on_delete=CASCADE)
    track = ForeignKey(Track, on_delete=CASCADE)
    sort_number = IntegerField()
    
    def __str__(self):
        return "{}; Track '{}' in Playlist '{}'".format(self.playlist.user.username, self.track.title, self.playlist.name)
