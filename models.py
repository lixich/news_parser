import datetime
from peewee import *

db = SqliteDatabase('news.db')


class BaseModel(Model):
    class Meta:
        database = db


class News(Model):
    text = CharField()
    url = TextField()
    created = DateField(default=datetime.date.today)

    class Meta:
        database = db
        db_table = 'news'


def create_tables():
    with db:
        db.create_tables([News])
