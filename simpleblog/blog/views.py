from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from braces.views import LoginRequiredMixin
from .models import Post


class PostActionMixin(object):
    def form_valid(self, form):
        msg = 'Post {0}!'.format(self.action)
        messages.info(self.request, msg)
        return super(PostActionMixin, self).form_valid(form)


class PostCreateView(LoginRequiredMixin, PostActionMixin, CreateView):
    model = Post
    action = 'created'

    template_name = 'blog/edit_post.html'


class PostUpdateView(LoginRequiredMixin, PostActionMixin, UpdateView):
    model = Post
    action = 'updated'

    template_name = 'blog/edit_post.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post.html'


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    queryset = Post.objects.order_by('-pub_date')[:5]
