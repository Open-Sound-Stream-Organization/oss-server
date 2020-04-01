from django.contrib.auth.models import User
from django.db.models import Model, CharField, TextField, ForeignKey, ManyToManyField, CASCADE, PROTECT, IntegerField, DateField, ImageField, FileField

class Tag(Model):
    name = CharField(max_length=1024)


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
    country_code = CharField(max_length=2, verbose_name='iso-3166-1-code', blank=True)


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
    area = ForeignKey(Area, on_delete=PROTECT, blank=True)
    begin = DateField("Date of persons birth/Date of group formation", blank=True)
    end = DateField("Death of person/Group dissolved - blank if still together", blank=True)
    user = ForeignKey(User, on_delete=CASCADE)
    tags = ManyToManyField(Tag)


class Album(Model):
    name = TextField()
    mbid = CharField(max_length=64, blank=True)
    release = DateField(blank=True)
    cover_url = CharField(max_length=1024, blank=True)
    cover_file = ImageField(blank=True)
    user = ForeignKey(User, on_delete=CASCADE)
    tags = ManyToManyField(Tag)

    def get_cover(self):
        if self.cover_file:
            return self.cover_file.url
        else:
            return self.cover_url


def audio_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Track(Model):
    title = CharField(max_length=512)
    mbid = CharField(max_length=64, blank=True)
    album = ForeignKey(Album, on_delete=CASCADE)
    user = ForeignKey(User, on_delete=CASCADE)
    artist = ManyToManyField(Artist)
    tags = ManyToManyField(Tag)
    audio = FileField(upload_to=audio_path, blank=True,
                       help_text=("Allowed type - .mp3, .wav, .ogg"))


class Playlist(Model):
    tracks = ManyToManyField(Track)
    tags = ManyToManyField(Tag)


class TrackInPlaylist(Model):
    playlist = ForeignKey(Playlist, on_delete=CASCADE)
    track = ForeignKey(Track, on_delete=CASCADE)
    sort_number = IntegerField()
