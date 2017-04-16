from __future__ import unicode_literals

from django.db import models


class Topic(models.Model):
    title = models.CharField(max_length=200)
    parent = models.ForeignKey('self', blank=True, null=True)
    children = models.ManyToManyField('self', blank=True, null=True)
    articles = models.ManyToManyField('Article', blank=True, null=True)
    depth = False

    def rows(self):
        articles = self.articles.all()
        return [articles[i:i + 3] for i in range(0, len(articles), 3)]

    def __str__(self):
        return self.title


class Article(models.Model):
    parent_topic = models.ForeignKey(Topic)
    title = models.TextField(max_length=200)
    summary = models.TextField()
    link = models.URLField()
    img = models.URLField()

    def __str__(self):
        return self.title
