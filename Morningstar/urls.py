"""Morningstar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import os
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from Morningstar import settings
from django.views.decorators.cache import cache_page
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import NavSitemap, BlogSitemap
sitemaps = {
    "blog": BlogSitemap,
    "nav": NavSitemap,
}


urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name="logout"),
    path('activate/', views.activate, name="activate"),
    path('registry/', views.registry, name="registry"),
    path('admin/', admin.site.urls, name="admin"),
    path('sms/', views.sms, name="sms"),
    path('sitemap.xml', cache_page(0)(sitemap), {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

    path('setKey/<str:value>/', views.setKey, name="setKey"),
    path('getKey/', cache_page(0)(views.getKey), name="getKey"),
    # app
    path('album/', include('album.urls')),
    path('blog/', include('blog.urls')),
    path('book/', include('book.urls')),
    path('forum/', include('forum.urls')),
    path('nav/', include('nav.urls')),
    path('poll/', include('poll.urls')),
    path('v2ray/', include('v2ray.urls')),

    # 其他
    re_path(r"media/(?P<path>.*)$", serve,
            {"document_root": settings.common.MEDIA_ROOT}),
    path('api-auth/', include('rest_framework.urls')),  # restful api
    path('__debug__/', include('debug_toolbar.urls')),

    # 快捷方式
    path('<slug:name>/', views.shortcut, name="shortcut"),
]
