from peewee import *

db = SqliteDatabase('news.db')


class BaseModel(Model):
    class Meta:
        database = db


class NewsModel(Model):
    title = CharField()
    url = TextField()
    created = DateTimeField()

    class Meta:
        database = db
        db_table = 'news'


def create_tables():
    with db:
        db.create_tables([NewsModel])
