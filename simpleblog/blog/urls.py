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
        regex=r'^post/(?P<slug>[-\w]+)$',
        view=views.PostDetailView.as_view(),
        name='blog_post_detail'
    ),
    url(
        regex=r'^new$',
        view=views.PostCreateView.as_view(),
        name='blog_post_new'
    ),
    url(
        regex=r'^edit/(?P<pk>\d+)$',
        view=views.PostUpdateView.as_view(),
        name='blog_post_edit'
    )

) # NOQA
