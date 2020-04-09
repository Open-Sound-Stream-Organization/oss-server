from tastypie.models import ApiKey as TastyApiKey
from django.db.models.fields import CharField

class ApiKey(TastyApiKey):
    purpose = CharField(max_length=1024, help_text="Describes where the API-Key is intended to be used")