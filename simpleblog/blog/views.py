import json
import datetime

from django import forms, http
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.template import Context, loader
from django.utils.encoding import force_unicode
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView

from braces.views import LoginRequiredMixin

from .models import Post, Comment
from .forms import PostForm, CommentForm


class PostActionMixin(object):
    def form_valid(self, form):
        msg = 'Post {0}!'.format(self.action)
        messages.info(self.request, msg)
        return super(PostActionMixin, self).form_valid(form)


class StaffRequiredMixin(object):
    """
Mixin allows you to require a user with `is_staff` set to True.
"""
    #adapted from SuperuserRequiredMixin from braces.views
    login_url = settings.LOGIN_URL  # LOGIN_URL from project settings
    raise_exception = False  # Default whether to raise an exception to none
    redirect_field_name = REDIRECT_FIELD_NAME  # Set by django.contrib.auth

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:  # If the user is a standard user,
            if self.raise_exception:  # *and* if an exception was desired
                raise PermissionDenied  # return a forbidden response.
            else:
                return redirect_to_login(request.get_full_path(),
                                         self.login_url,
                                         self.redirect_field_name)

        return super(StaffRequiredMixin, self).dispatch(request,
            *args, **kwargs)


class PostCreateView(LoginRequiredMixin, StaffRequiredMixin, PostActionMixin, CreateView):
    form = PostForm
    model = Post
    action = 'created'

    def get_initial(self):
        initial = super(PostCreateView, self).get_initial()
        initial['pub_date'] = datetime.date.today()
        return initial


class PostUpdateView(LoginRequiredMixin, StaffRequiredMixin, PostActionMixin, UpdateView):
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
    queryset = Post.objects.order_by('-pub_date', '-created')
    paginate_by = 4


class PostDeleteView(LoginRequiredMixin, StaffRequiredMixin, PostActionMixin, DeleteView):
    model = Post
    action = 'deleted'
    success_url = '/'


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
