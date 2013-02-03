import json

from django import forms, http
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.template import Context, loader
from django.utils.encoding import force_unicode

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

        normal_retval = super(CommentCreateView, self).form_valid(form)

        if self.request.POST.get('format', 'html') != 'json':
            return normal_retval

        t = loader.get_template('blog/comment.html')
        context = Context(self.get_context_data())

        return self.get_json_response(
            json.dumps({
                'success': True,
                'messages': [{'message': m.message, 'tags': m.tags} for m in
                             messages.get_messages(self.request)],
                'comment': t.render(context)

            })
        )

    def form_invalid(self, form):
        normal_retval = super(CommentCreateView, self).form_invalid(form)
        if self.request.POST.get('format', 'html') != 'json':
            return normal_retval

        return self.get_json_response(
            json.dumps({
                'success': False,
                'errors': {k: v.as_ul() if len(v) > 1 else force_unicode(v[0]) for k, v in form.errors.iteritems()}
            })
        )

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)
