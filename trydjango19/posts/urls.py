from django.conf.urls import url
from django.contrib import admin

from .views import (
    post_create,
    post_delete,
    post_detail,
    post_list,
    post_update
)

# refer to the first come url
urlpatterns = [
    url(r'^$', post_list),
    url(r'^create/$', post_create),
    # url that accept id as param, and only accept digin (d+)
    url(r'^detail/(?P<id>\d+)/$', post_detail),
    url(r'^update/$', post_update),
    url(r'^delete/$', post_delete),

]