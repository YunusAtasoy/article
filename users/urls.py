# Django
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.conf.urls import url, include
from . import views
from .views import *

# Local Django
from users.views import UserView


urlpatterns = [
    # Admin
    url(r'^admin/', admin.site.urls),
    # Pages
    url(r'^$', UserView.as_view(), name='register'),
]
