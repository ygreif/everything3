import csv
import datetime
import pprint
import random
import re

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError

from articles.models import Article
from django_slack import slack_message

pp = pprint.PrettyPrinter()


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        articles = Article.objects.all()
        article = random.choice(articles)
        slack_message('articles/throwback.slack', {'article': article})
