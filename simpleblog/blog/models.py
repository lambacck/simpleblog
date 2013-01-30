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


class Comment(TimeStampedModel, models.Model):
    post = models.ForeignKey(Post)

    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
