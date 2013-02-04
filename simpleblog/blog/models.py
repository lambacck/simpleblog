from django.db import models

from model_utils.models import TimeStampedModel


class Post(TimeStampedModel, models.Model):
    title = models.CharField(max_length=100, verbose_name='Post Title')
    slug = models.SlugField(unique=True)
    pub_date = models.DateField(verbose_name='Publication Date')
    body = models.TextField(verbose_name="Post Content")

    @models.permalink
    def get_absolute_url(self):
        url_data = {
            'slug': self.slug,
        }
        return ('blog_post_detail', (), url_data)

    def get_next_link(self):
        try:
            obj = self.get_next_by_pub_date()
        except self.DoesNotExist:
            return None

        return obj.get_absolute_url()

    def get_previous_link(self):
        try:
            obj = self.get_previous_by_pub_date()
        except self.DoesNotExist:
            return None

        return obj.get_absolute_url()


class Comment(TimeStampedModel, models.Model):
    post = models.ForeignKey(Post)

    name = models.CharField(max_length=255, verbose_name='Your name')
    email = models.EmailField(verbose_name='Email Address (only used for gravatar)')
    body = models.TextField(verbose_name='Comment')

    def get_absolute_url(self):
        return self.post.get_absolute_url() + '#comment-%(id)d' % {'id': self.id}
