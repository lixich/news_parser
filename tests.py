import json
import config
from unittest import TestCase
from datetime import datetime
from app import app
from scheduler import parse_news


class UnitTestsParseNews(TestCase):

    def test_parse_news_data_structure_and_format(self):
        # Arrange.
        fields = ['title', 'url', 'created']
        type_fields = [str, str, str]
        created_format = '%Y-%m-%dT%H:%M:%S.%f'
        # Act.
        news_dicts = parse_news()
        # Asserts.
        self.assertEqual(list, type(news_dicts), 'Incorrect type of posts')
        for one_news in news_dicts:
            self.assertEqual(set(fields), set(one_news.keys()), "Incorrect posts fields")
            for filed, field_type in zip(fields, type_fields):
                self.assertNotEqual('', one_news.get(filed))
                self.assertEqual(field_type, type(one_news.get(filed)))
            self.assertEqual(datetime, type(datetime.strptime(one_news.get('created'), created_format)))

    def test_parse_news_data_size(self):
        # Act.
        news_dicts = parse_news()
        # Asserts.
        self.assertEqual(list, type(news_dicts), 'Incorrect type of posts')
        self.assertEqual(config.PARSER_NEWS_COUNT, len(news_dicts), 'Incorrect posts count')


class SociableUnitTestsHandlerNews(TestCase):

    def setUp(self):
        # TODO add test db
        # self.app.config.SQLITE_DATABASE_NAME = config.SQLITE_TEST_DATABASE_NAME
        self.app = app.test_client()
        self.app.testing = True

    def test_update_news_data_structure_and_format(self):
        # Arrange.
        fields = ['title', 'url', 'created']
        type_fields = [str, str, str]
        created_format = '%Y-%m-%dT%H:%M:%S.%f'
        # Act.
        result = self.app.get('/posts/update')
        # Asserts.
        self.assertEqual(result.status_code, 200)
        news_dicts = json.loads(result.get_data())
        self.assertEqual(list, type(news_dicts), 'Incorrect type of posts')
        for one_news in news_dicts:
            self.assertEqual(set(fields), set(one_news.keys()), "Incorrect posts fields")
            for filed, field_type in zip(fields, type_fields):
                self.assertNotEqual('', one_news.get(filed))
                self.assertEqual(field_type, type(one_news.get(filed)))
            self.assertEqual(datetime, type(datetime.strptime(one_news.get('created'), created_format)))

    def test_get_news_data_structure_and_format(self):
        # Arrange.
        fields = ['id', 'title', 'url', 'created']
        type_fields = [int, str, str, str]
        created_format = '%Y-%m-%dT%H:%M:%S.%f'
        # Act.
        result = self.app.get('/posts')
        # Asserts.
        self.assertEqual(result.status_code, 200)
        news_dicts = json.loads(result.get_data())
        self.assertEqual(list, type(news_dicts), 'Incorrect type of posts')
        for one_news in news_dicts:
            self.assertEqual(set(fields), set(one_news.keys()), "Incorrect posts fields")
            for filed, field_type in zip(fields, type_fields):
                self.assertNotEqual('', one_news.get(filed), "Empty field's value")
                self.assertEqual(field_type, type(one_news.get(filed)), "Incorrect field's type")
            self.assertEqual(datetime, type(datetime.strptime(one_news.get('created'), created_format)), 'Incorrect date format')

    def test_get_news_data_order(self):
        # Arrange.
        fields = ['id', 'title', 'url', 'created']
        # Act.
        for field in fields:
            with self.subTest(order=field):
                result = self.app.get(f'/posts?order={field}')
                # Asserts.
                self.assertEqual(result.status_code, 200)
                news_dicts = json.loads(result.get_data())
                for i in range(len(news_dicts)-1):
                    self.assertTrue(news_dicts[i][field] <= news_dicts[i+1][field], 'Incorrect sorting')

    def test_get_news_incorrect_order(self):
        # Act.
        result = self.app.get('/posts?order=other_field')
        # Asserts.
        self.assertEqual(result.status_code, 400)
        error = json.loads(result.get_data())
        self.assertEqual(error['message'], 'Field "order" is incorrect')

    def test_get_news_data_order_with_desc(self):
        # Arrange.
        fields = ['id', 'title', 'url', 'created']
        # Act.
        for field in fields:
            with self.subTest(order=field):
                result = self.app.get(f'/posts?desc=true&order={field}')
                # Asserts.
                self.assertEqual(result.status_code, 200)
                news_dicts = json.loads(result.get_data())
                for i in range(len(news_dicts)-1):
                    self.assertTrue(news_dicts[i][field] >= news_dicts[i+1][field], 'Incorrect sorting')

    def test_get_news_default_size(self):
        # Arrange.
        default_size = 5
        # Act.
        result = self.app.get('/posts')
        # Asserts.
        self.assertEqual(result.status_code, 200)
        news_dicts = json.loads(result.get_data())
        self.assertEqual(default_size, len(news_dicts), 'Incorrect default size of posts')

    def test_get_news_acceptable_limit(self):
        # Arrange.
        acceptable_size = 250
        # Act.
        result = self.app.get('/posts')
        # Asserts.
        self.assertEqual(result.status_code, 200)
        news_dicts = json.loads(result.get_data())
        self.assertTrue(acceptable_size >= len(news_dicts), 'Incorrect default size of posts')

    def test_get_news_not_acceptable_limit(self):
        # Act.
        result = self.app.get('/posts?limit=1000')
        # Asserts.
        self.assertEqual(result.status_code, 400)
        error = json.loads(result.get_data())
        self.assertEqual(error['message'], '"limit" is too long')

    def test_get_news_big_offset(self):
        # Act.
        result = self.app.get('/posts?offset=100000000')
        # Asserts.
        self.assertEqual(result.status_code, 200)
        empty_list = json.loads(result.get_data())
        self.assertEqual([], empty_list)
