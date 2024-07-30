from __future__ import unicode_literals

import random
from django.core.management.base import BaseCommand
from django.db.models import Max
from articles.models import Article
from django_slack import slack_message

class Command(BaseCommand):
    help = 'Sends a random throwback article to the Slack channel'

    def handle(self, *args, **options):
        article = self.get_random_article()

        if article:
            self.send_to_slack(article)
            self.stdout.write(self.style.SUCCESS('Successfully sent throwback article: {0}'.format(article.title)))
        else:
            self.stdout.write(self.style.WARNING('No suitable throwback articles found'))

    def get_random_article(self):
        # Get the maximum ID
        max_id = Article.objects.aggregate(Max('id'))['id__max']

        if max_id is None:
            return None

        # Assume we want articles from the first 90% of the ID range as throwbacks
        throwback_max_id = int(max_id * 0.9)

        # Get all articles up to the throwback_max_id
        throwback_articles = Article.objects.filter(id__lte=throwback_max_id)

        if not throwback_articles.exists():
            return None

        return random.choice(throwback_articles)

    def send_to_slack(self, article):
        context = {
            'article': article,
            'is_throwback': True
        }
        slack_message('articles/article.slack', context)
