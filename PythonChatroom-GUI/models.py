from datetime import datetime

from peewee import *

db = SqliteDatabase('db.sqlite')


class BaseModel(Model):
    class Meta:
        database = SqliteDatabase('db.sqlite')


class SavedMessage(BaseModel):
    _id = IntegerField(primary_key=True)
    username = CharField(max_length=255)
    content = TextField()
    timestamp = DateTimeField(default=datetime.now)

    class Meta:
        table_name = 'saved_messages'


db.create_tables([SavedMessage])
