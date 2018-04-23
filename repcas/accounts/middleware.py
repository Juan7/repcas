from . import models

class RequestCookiesMiddleware(object):
    """Sets or destroys cookies on the request cookies list."""

    def __init__(self, get_response):
        """One-time configuration and initialization."""
        self.get_response = get_response

    def _set_cookies(self, request, response):
        """Set cookies from request to response."""
        try:
            for cookie in request.set_cookies:
                response.set_cookie(**cookie)
        except AttributeError:
            pass

    def _delete_cookies(self, request, response):
        """Delete cookies from request to response."""
        try:
            for cookie in request.delete_cookies:
                response.delete_cookie(**cookie)
        except AttributeError:
            pass

    def __call__(self, request):
        """Code to be executed for each request before and after the view is called."""
        response = self.get_response(request)

        self._set_cookies(request, response)
        self._delete_cookies(request, response)

        return response


class ProfileMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        profile = None

        if request.user.is_authenticated:
            client_pk = request.COOKIES.get('client_pk')
            try:
                # import pdb; pdb.set_trace()
                profile = models.Profile.objects.select_related(
                    'client',
                    'user').get(
                    client__pk=client_pk,
                    user=request.user,
                    is_active=True,
                    client__is_active=True)

            except models.Profile.DoesNotExist:
                pass

        request.profile = profile
        response = self.get_response(request)
        return response
