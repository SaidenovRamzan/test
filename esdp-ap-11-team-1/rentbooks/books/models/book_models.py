from mongoengine import (
    Document,
    StringField,
    IntField,
    BooleanField,
    ReferenceField,
    SequenceField,
    ImageField,
    signals,
)
from elastic.document import CompositionElastic
from elasticsearch_dsl import connections
import logging


class Genres(Document):
    name = StringField()


class Composition(Document):
    id_Composition = SequenceField(primary_key=True)
    name = StringField()
    author = StringField()
    description = StringField()
    rent_qte = IntField(default=0)
    language = StringField()
    id_genre = ReferenceField(Genres)
    is_visible = BooleanField(default=False)

    def __str__(self):
        return f"{self.id_Composition} {self.name}"

    @classmethod
    def post_save(cls, sender, document, **kwargs):
        logging.info(f"{document.name} {'saved '}")
        connections.create_connection(hosts=["http://elasticsearch1:9200"])
        CompositionElastic.init()
        CompositionElastic(
            meta={"id": document.id_Composition},
            name=document.name,
            description=document.description,
            author=document.author,
            genre=document.id_genre.name,
        ).save()

    @classmethod
    def post_delete(cls, sender, document, **kwargs):
        logging.info(f"{document.name} {'dleted '}")
        connections.create_connection(hosts=["http://elasticsearch1:9200"])
        CompositionElastic.get(id=document.id_Composition).delete()


signals.post_save.connect(Composition.post_save, sender=Composition)
signals.post_delete.connect(Composition.post_delete, sender=Composition)


class Book(Document):
    id_Book = SequenceField(primary_key=True)
    id_composition = ReferenceField(Composition)
    year = IntField()
    izdatelstvo = StringField()
    pages = IntField()
    coverphoto = ImageField()
    isbn = StringField()

    def __str__(self):
        return f"{self.isbn}"

    def get_image_url(self):
        if (
            self.coverphoto and self.coverphoto.grid_id
        ):  # Проверяем, есть ли у нас изображение и его идентификатор
            # Здесь вы должны использовать ваш способ формирования URL-адреса к изображению в GridFS
            # Например, если вы используете Django Storage для GridFS, вы можете сделать следующим образом:
            from django.core.files.storage import default_storage

            return default_storage.url(str(self.coverphoto.grid_id))
        else:
            return None
