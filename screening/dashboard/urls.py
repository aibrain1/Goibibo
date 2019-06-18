from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^suggestion-search/$',views.suggestionSearch, name='suggestion-search'),
]
