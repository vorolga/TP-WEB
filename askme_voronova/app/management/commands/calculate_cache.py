from django.core.cache import cache
from django.core.management.base import BaseCommand
from app.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        rating = Tag.objects.best_tags()
        cache.set('best_tags', rating, 86400 + 500)
        authors = Profile.objects.best_users()
        cache.set('best_users', authors, 86400 + 500)
