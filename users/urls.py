# Django
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.conf.urls import url, include
from . import views
from .views import *

# Local Django
from users.views import UserView, IndexView, DetailView


urlpatterns = [
    # Admin
    url(r'^admin/', admin.site.urls),
    # Pages
    url(r'^$', UserView.as_view(), name='register'),
    url(r'index/$', IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', DetailView.as_view(), name = 'detail'),
    url(r'^(?P<pk>[-\w]+)/comments/$',views.post_new, name='edit'),
    url(r'^activation/(?P<key>.+)$', views.activation, name='activation'),
    url(r'^logout/',views.user_logout),
    url(r'^password_change/$', views.change_password, name='password_change'),
]
