from peewee import *
from config import SQLITE_DATABASE_NAME

db = SqliteDatabase(SQLITE_DATABASE_NAME)


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

    @staticmethod
    def get_fields():
        return NewsModel._meta.sorted_field_names


def create_tables():
    with db:
        db.create_tables([NewsModel])
