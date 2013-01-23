from django.db import models
from model_utils.models import TimeStampedModel


class Post(TimeStampedModel, models.Model):
    pub_date = models.DateField()
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique_for_date='pub_date')
    body = models.TextField()

    @models.permalink
    def get_absolute_url(self):
        pub_date = self.pub_date
        url_data = {
            'slug': self.slug,
            'date': pub_date.isoformat(),
        }
        return ('post_detail', (), url_data)


class Comment(TimeStampedModel, models.Model):
    post = models.ForeignKey(Post)

    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
