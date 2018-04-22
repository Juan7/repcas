from django.conf import settings


def set_cookie(request, key, value):
    cookie = {
        'key': key,
        'value': value,
        'max_age': settings.SESSION_COOKIE_AGE
    }
    try:
        request.set_cookies
    except AttributeError:
        request.set_cookies = []
    request.set_cookies.append(cookie)
