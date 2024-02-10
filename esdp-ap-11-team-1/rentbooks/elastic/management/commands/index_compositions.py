# your_app_name/management/commands/index_compositions.py

from django.core.management.base import BaseCommand
from elasticsearch_dsl import connections
from books.models import Composition
from elastic.document import CompositionElastic
import logging


class Command(BaseCommand):
    help = 'Index compositions in Elasticsearch'

    def handle(self, *args, **options):
        connections.create_connection(hosts=['http://elasticsearch1:9200'])
        CompositionElastic.init()
        logging.info("Index compositions in Elasticsearch")
        for composition in Composition.objects.all():
            CompositionElastic(meta={'id': composition.id}, name=composition.name, description=composition.description, author=composition.author, genre=composition.id_genre.name).save()
        self.stdout.write(self.style.SUCCESS('Successfully indexed compositions'))
