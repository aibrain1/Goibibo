from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addStock', views.addStock, name='addStock'),
    path('jsonParser/', views.jsonParserView, name='jsonParser'),
    path('jsonAction/', views.jsonLoadAndParse, name='jsonAction'),
    re_path(r'^$',views.index, name='home'),
    re_path(r'^suggestion-search/$',views.suggestionSearch, name='suggestion-search'),
]
