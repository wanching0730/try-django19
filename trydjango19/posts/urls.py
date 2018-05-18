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
    # included named URL 'detail'
    url(r'^detail/(?P<id>\d+)/$', post_detail, name='detail'),
    url(r'^update/(?P<id>\d+)/$', post_update, name='update'),
    url(r'^delete/$', post_delete),

]