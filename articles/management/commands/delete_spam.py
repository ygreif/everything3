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

    def handle(self, *args, **options):
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        articles = Article.objects.all().filter(
            link__contains='youtu.be').delete()
