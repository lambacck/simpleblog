from django.forms import ModelForm

from .models import Post, Comment


class PostForm(ModelForm):

    class Meta:
        model = Post


class CommentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            widget = field.widget

            html_class = widget.attrs.get('class', '')
            if html_class:
                html_class += ' '

            html_class += 'required'

            if name == 'email':
                html_class += ' email'

            widget.attrs['class'] = html_class

    class Meta:
        model = Comment
