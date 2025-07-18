import unittest
from peewee import *

from app import TimelinePost

MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestDatabase(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        test_db.drop_tables(MODELS)
        test_db.close()

    def test_timeline_post(self):
        first_post = TimelinePost.create(name="John Doe", 
        email="John22@gmail.com", content="Hi Mom!")
        assert first_post.id == 1
        second_post = TimelinePost.create(name="Jane Doe",
        email="jane23@hotmail.com", content="Hello World!")
        assert second_post.id == 2

        get_first_post = TimelinePost.get(TimelinePost.id == 1)
        assert get_first_post.name == "John Doe"
        get_second_post = TimelinePost.get(TimelinePost.id == 2)
        assert get_second_post.name == "Jane Doe"