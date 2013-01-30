from django import forms
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from braces.views import LoginRequiredMixin
from .models import Post, Comment
from .forms import PostForm, CommentForm


class PostActionMixin(object):
    def form_valid(self, form):
        msg = 'Post {0}!'.format(self.action)
        messages.info(self.request, msg)
        return super(PostActionMixin, self).form_valid(form)


class PostCreateView(LoginRequiredMixin, PostActionMixin, CreateView):
    form = PostForm
    model = Post
    action = 'created'


class PostUpdateView(LoginRequiredMixin, PostActionMixin, UpdateView):
    form = PostForm
    model = Post
    action = 'updated'


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = context['form'] = CommentForm(initial={'post': context['post'].id})
        form.fields['post'].widget = forms.HiddenInput()

        post = context['post']
        comments = post.comment_set.order_by('modified')
        context['comments'] = comments

        return context


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    queryset = Post.objects.order_by('-pub_date', '-modified')[:5]


class CommentCreateView(CreateView):
    model = Comment
    form = CommentForm

    def form_valid(self, form):
        msg = 'Thanks for your comment!'
        messages.info(self.request, msg)
        return super(CommentCreateView, self).form_valid(form)
