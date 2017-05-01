"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from webblog import views

urlpatterns = [
    url(r'^$', views.index1, name='views-index1'),
    url(r'^new_post/', views.new_post1, name='views-new_post1'),
    url(r'^post_detail1/', views.post_detail1, name='views-post_detail1'),
    url(r'^post/(?P<post_id>[0-9]+)', views.post_detail, name='views-post-detail'),
    url(r'^register/', views.register1, name='views-register_user1'),
    url(r'^logout/', views.logout_page, name='views-logout'),
    url(r'^login/', views.login1, name='views-login1'),
]
