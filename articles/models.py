from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Topic(MPTTModel):
    title = models.TextField(max_length=200)
    parent = TreeForeignKey(
        'self', blank=True, null=True, related_name='children')
    articles = models.ManyToManyField('Article', blank=True, null=True)
    depth = False

    def rows(self):
        articles = self.articles.all()
        return [articles[i:i + 2] for i in range(0, len(articles), 2)]

    def __str__(self):
        return self.title

    @property
    def allow_new(self):
        return 'everything!' not in self.title and 'Corporate ETR' not in self.title

    @property
    def channel(self):
        if 'covid' in self.title.lower() or 'coronavirus' in self.title.lower():
            return 'coronavirus'
        else:
            return 'feed'

class Article(models.Model):
    parent_topic = models.ForeignKey(Topic)
    title = models.TextField(max_length=200)
    summary = models.TextField()
    link = models.URLField(blank=True)
    img = models.URLField(blank=True)

    def __str__(self):
        return self.title

    def is_spam(self):
        return not self.parent_topic.allow_new


class Stub(models.Model):
    classified = models.BooleanField(default=False)
    title = models.TextField(max_length=200)
    link = models.TextField()
    sender = models.CharField(max_length=200)

    def __str__(self):
        return ' - '.join([self.title, self.link, self.sender])
