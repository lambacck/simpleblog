from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'simpleblog.views.home', name='home'),
    url(
        regex=r'^$',
        view=views.PostListView.as_view(),
        name='blog_home'
    ),

    url(
        regex=r'^(?P<date>\d{4}-\d{2}-\d{2})/(?P<slug>[-\w]+)$',
        view=views.PostDetailView,
        name='blog_post_details'
    ),

) # NOQA
