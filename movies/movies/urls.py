"""
URL configuration for movies project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.template.defaulttags import url

from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from movies_database.views import MovieViewSet, UserMovieRelationViews, ShortInfoMovieViewSet, PersonInfoViewSet, \
    ProfessionViewSet

router = SimpleRouter()
router.register(r'movie', MovieViewSet)
router.register(r'movie_short', ShortInfoMovieViewSet)
router.register(r'movie_relation', UserMovieRelationViews)
router.register(r'profs', ProfessionViewSet)
router.register(r'persons', PersonInfoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('social_django.urls', namespace='social'), current_movie_info),
    path("__debug__/", include("debug_toolbar.urls")),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

urlpatterns += router.urls
