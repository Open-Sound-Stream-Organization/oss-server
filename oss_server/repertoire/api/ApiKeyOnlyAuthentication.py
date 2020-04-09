from tastypie.models import ApiKey
from tastypie.http import HttpUnauthorized
from tastypie.authentication import Authentication
from django.core.exceptions import ObjectDoesNotExist

class ApiKeyOnlyAuthentication(Authentication):
    def is_authenticated(self, request, **kwargs):
        if not(request.META.get('HTTP_AUTHORIZATION')):
            return HttpUnauthorized()
        api_key_str = request.META['HTTP_AUTHORIZATION']
        try:
            api_key = ApiKey.objects.get(key=api_key_str)
        except ObjectDoesNotExist:
            return HttpUnauthorized()
        request.user = api_key.user
        return True
