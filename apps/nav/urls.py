from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'nav'
urlpatterns = [
    path('', cache_page(60*5)(views.index), name='index'),
    path('config/', views.config_api, name='config'),
    path('me/', views.me, name="me"),
    path('resource/<slug:name>/', cache_page(60*5)
         (views.resource), name='resource'),
]
