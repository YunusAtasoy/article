# Django
from django.conf.urls import url

# Local Django
from magazines.views import MagazineDetails, MagazinesList


urlpatterns = [
    url(r'^magazines-list/subject/(?P<category>)/$',
        MagazinesList.as_view(),
        name="magazines_list"),
    url(r'^magazine/(?P<pk>[0-9]+)/details/$',
        MagazineDetails.as_view(),
        name="magazine_details"),
]
