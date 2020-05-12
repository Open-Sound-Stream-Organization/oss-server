from typing import Union, List

from tastypie.authentication import Authentication


class RestrictToMethod(Authentication):
    def __init__(self, authentication : Authentication, method: Union[str, List[str]] = 'DELETE'):
        super().__init__()
        if type(method) == str:
            method = [method]
        self.method = method
        self.auth = authentication

    def is_authenticated(self, request, **kwargs):
        if request.method in self.method:
            return self.auth.is_authenticated(request, **kwargs)
        else:
            return False