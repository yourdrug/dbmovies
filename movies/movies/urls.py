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
from django.conf.urls.static import static
from django.contrib import admin
from django.template.defaulttags import url
from django.conf import settings

from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from account.views import AccountListView, FileUploadAPIView
from movies_database.views import MovieViewSet, UserMovieRelationViews, ShortInfoMovieViewSet, PersonInfoViewSet, \
    ProfessionViewSet, UserMovieRelationForPersonView, SearchAPIView

router = SimpleRouter()
router.register(r'movie', MovieViewSet, basename='movie')
router.register(r'movie_short', ShortInfoMovieViewSet)
router.register(r'movie_relation', UserMovieRelationViews)
router.register(r'user_movie_relation', UserMovieRelationForPersonView, basename='user_info')
router.register(r'profs', ProfessionViewSet)
router.register(r'persons', PersonInfoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('search/', SearchAPIView.as_view()),
    path('users/', AccountListView.as_view()),
    path("__debug__/", include("debug_toolbar.urls")),
    path('auth/', include('djoser.urls')),
    path('social/', include('chatting.urls')),
    path('users_update/', FileUploadAPIView.as_view()),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

urlpatterns += router.urls

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
