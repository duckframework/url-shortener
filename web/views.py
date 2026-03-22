"""
Views for the URL shortener.

- home - renders the shortener HomePage
- redirect - looks up the short code, increments clicks, redirects
"""
from duck.settings import SETTINGS
from duck.utils.path import joinpaths
from duck.shortcuts import to_response, redirect, not_found404
from duck.http.response import HttpResponse, FileResponse

from web.ui.pages.home import HomePage


def robots(request):
    """
    View for serving a robots.txt file.
    """
    robots_txt = joinpaths(SETTINGS['BASE_DIR'], "etc/robots.txt")
    return FileResponse(robots_txt)
    
    
def favicon(request):
    """
    View for serving a favicon.
    """
    if SETTINGS['DEBUG']:
        favicon = joinpaths(SETTINGS['BASE_DIR'], "web/ui/static/images/favicon.ico")
    else:
        favicon = joinpaths(SETTINGS['STATIC_ROOT'], "images/favicon.ico")
    return FileResponse(favicon)


def home(request):
    """
    Entry view for the web application.
    """
    page = HomePage(request=request)
    return to_response(page)


def redirect_short_url(request, short_code: str):
    """
    Resolves a short code to its original URL, increments the click
    counter, and issues a 301 redirect.
    Returns 404 if the code doesn't exist.
    """
    from web.backend.django.duckapp.core.models import ShortURL

    try:
        short = ShortURL.objects.get(short_code=short_code)
    except ShortURL.DoesNotExist:
        return not_found404(body="Short URL not found.")

    short.increment_clicks()
    return redirect(short.original_url, permanent=False)
