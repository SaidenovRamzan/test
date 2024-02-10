from mongoengine import Document, StringField, IntField, BooleanField, ReferenceField, SequenceField, ImageField
from elastic.document import CompositionElastic
from elasticsearch_dsl import connections


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        connections.create_connection(hosts=['http://elasticsearch1:9200'])
        CompositionElastic.init()
        CompositionElastic(meta={'id': self.id_Composition}, name=self.name, description=self.description, author=self.author, genre=self.id_genre.name).save()
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)  # Вызов родительского метода delete
        connections.create_connection(hosts=['http://elasticsearch1:9200'])
        CompositionElastic.get(id=self.id_Composition).delete()


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
        if self.coverphoto and self.coverphoto.grid_id:  # Проверяем, есть ли у нас изображение и его идентификатор
            # Здесь вы должны использовать ваш способ формирования URL-адреса к изображению в GridFS
            # Например, если вы используете Django Storage для GridFS, вы можете сделать следующим образом:
            from django.core.files.storage import default_storage
            return default_storage.url(str(self.coverphoto.grid_id))
        else:
            return None 
