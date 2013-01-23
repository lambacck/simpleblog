from django.db import models
from model_utils.models import TimeStampedModel


class Post(TimeStampedModel, models.Model):
    pub_date = models.DateField()
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique_for_date='pub_date')
    body = models.TextField()


class Comment(TimeStampedModel, models.Model):
    post = models.ForeignKey(Post)

    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
