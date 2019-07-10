from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url('^$',views.index,name='index'),
    url(r'^search/',views.search_category, name='search_results'),
    url(r'^tractor/(\d+)',views.tractor_details,name='tractor_details'),
    url(r'^location/(\d+)',views.filter_by_location,name='located_images'),
    url(r'^new/tractor/$',views.new_tractor,name='new-tractor'),
    url(r'^profile/$',views.profile,name='profile'),
    url(r'^new_profile/$',views.new_profile,name = 'new_profile'),
    url(r'^edit/profile/$',views.profile_edit,name = 'edit_profile'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)