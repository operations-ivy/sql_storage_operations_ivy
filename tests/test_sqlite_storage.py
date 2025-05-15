import unittest

from sql_storage_operations_ivy.sqlite_storage import SqliteStorage

import datetime

class TestSqliteStorage(unittest.TestCase):

    def setUp(self):
        self.storage = SqliteStorage(":memory:")
        self.create_table()

    def tearDown(self):
        self.storage.close_connection()

    def create_table(self):
        create_table_sql = """
        CREATE TABLE chuck (
            id TEXT PRIMARY KEY,
            category TEXT,
            value TEXT,
            timestamp DATETIME
        )
        """
        self.storage.cursor.execute(create_table_sql)
        self.storage.conn.commit()

    def test_insert_and_read_all_jokes(self):
        self.storage.insert_joke("123", "funny", "Why did the chicken cross the road?")
        jokes = self.storage.read_all_jokes()
        self.assertEqual(len(jokes), 1)
        self.assertEqual(jokes[0][0], "123")
        self.assertEqual(jokes[0][1], "funny")
        self.assertEqual(jokes[0][2], "Why did the chicken cross the road?")
        self.assertIsInstance(jokes[0][3], str | datetime.datetime)

    def test_check_for_duplicate_true(self):
        self.storage.insert_joke("456", "dad", "I'm on a seafood diet. I see food and I eat it.")
        is_duplicate = self.storage.check_for_duplicate("456", "I'm on a seafood diet. I see food and I eat it.")
        self.assertTrue(is_duplicate)

    def test_check_for_duplicate_false(self):
        self.storage.insert_joke("789", "tech", "There are 10 types of people in the world...")
        is_duplicate = self.storage.check_for_duplicate("999", "This is not a joke.")
        self.assertFalse(is_duplicate)

    def test_get_joke_id_by_value_found(self):
        self.storage.insert_joke("abc", "classic", "Knock knock.")
        joke_id = self.storage.get_joke_id_by_value("Knock knock.")
        self.assertEqual(joke_id[0], "abc")

    def test_get_joke_id_by_value_not_found(self):
        joke_id = self.storage.get_joke_id_by_value("This joke doesn't exist.")
        self.assertIsNone(joke_id)


if __name__ == '__main__':
    unittest.main()
