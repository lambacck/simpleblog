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
    ),
    url(
        regex=r'^delete/(?P<pk>\d+)$',
        view=views.PostDeleteView.as_view(),
        name='blog_post_delete'
    ),
    url(
        regex=r'^newcomment$',
        view=views.CommentCreateView.as_view(),
        name='blog_comment_new'
    ),

) # NOQA
