from mongoengine import Document, StringField, IntField, ReferenceField, SequenceField, DateTimeField
from datetime import datetime

class Chat(Document):
    id = SequenceField(primary_key=True)
    user_1 = IntField()
    user_2 = IntField()
    user_shelf = IntField()
    
    
class Message(Document):
    id = SequenceField(primary_key=True)
    chat = ReferenceField(Chat)
    sender = IntField()
    recipient = IntField()
    user_shelf = IntField()
    message = StringField()
    created_at = DateTimeField(default=datetime.now)
