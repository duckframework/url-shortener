"""
URL patterns for the URL shortener.
"""
from duck.urls import path, re_path

from web import views

urlpatterns = [
    path("/", views.home, name="home"),
    path("/s/<short_code>", views.redirect_short_url, name="redirect"),
]
