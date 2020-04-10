from django.contrib.auth.models import User
from django.db.models import ForeignKey, CASCADE, BooleanField
from tastypie.models import ApiKey as TastyApiKey
from django.db.models.fields import CharField
from secrets import token_urlsafe

class ApiKey(TastyApiKey):
    user = ForeignKey(User, on_delete=CASCADE, help_text='Multiple Keys per User are possible')
    purpose = CharField(max_length=1024, help_text="Describes where the API-Key is intended to be used", blank=False)
    key = CharField(max_length=512, blank=True, default='', db_index=True)
    shown = BooleanField(verbose_name='Wether the user has seen the API-Key', default=False)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(ApiKey, self).save(*args, **kwargs)

    def generate_key(self):
        return token_urlsafe(128)

    def __str__(self):
        return "{}: {}".format(self.user, self.purpose)