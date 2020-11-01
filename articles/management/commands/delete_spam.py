import csv
import datetime
import pprint
import re

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError

from articles.models import Article

pp = pprint.PrettyPrinter()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--execute', action='store_true')
        parser.add_argument('--r', type=str)

    def handle(self, *args, **options):
        execute = options.get('execute')
        r = options.get('r')

        articles = Article.objects.all().filter(
            title__contains=r)
        if not execute:
            for a in articles:
                print a
        else:
            print "Deleting", len(articles)
            articles.delete()
