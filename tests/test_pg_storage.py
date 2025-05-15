import os
import datetime
import pytest

from sql_storage_operations_ivy.pg_storage import PGStorage

@pytest.fixture(scope="function")
def pg_storage():
    db_conn_string = os.environ["TEST_DB_URL"]
    storage = PGStorage(db_conn_string)

    with storage.conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chuck (
                id TEXT PRIMARY KEY,
                category TEXT,
                value TEXT,
                timestamp TIMESTAMP
            )
        """)
        cur.execute("DELETE FROM chuck")
        storage.conn.commit()

    yield storage
    storage.close_connection()


def test_insert_and_read_all_jokes(pg_storage):
    pg_storage.insert_joke("123", "funny", "Why did the chicken cross the road?")
    jokes = pg_storage.read_all_jokes()

    assert len(jokes) == 1
    assert jokes[0][0] == "123"
    assert jokes[0][1] == "funny"
    assert jokes[0][2] == "Why did the chicken cross the road?"
    assert isinstance(jokes[0][3], datetime.datetime)


def test_check_for_duplicate_true(pg_storage):
    pg_storage.insert_joke("456", "dad", "I'm on a seafood diet. I see food and I eat it.")
    is_duplicate = pg_storage.check_for_duplicate("456", "I'm on a seafood diet. I see food and I eat it.")
    assert is_duplicate is True


def test_check_for_duplicate_false(pg_storage):
    pg_storage.insert_joke("789", "tech", "There are 10 types of people...")
    is_duplicate = pg_storage.check_for_duplicate("999", "This is a unique joke.")
    assert is_duplicate is False


def test_get_joke_id_by_value_found(pg_storage):
    pg_storage.insert_joke("abc", "classic", "Knock knock.")
    joke_id = pg_storage.get_joke_id_by_value("Knock knock.")
    assert joke_id[0] == "abc"


def test_get_joke_id_by_value_not_found(pg_storage):
    joke_id = pg_storage.get_joke_id_by_value("This one doesn't exist.")
    assert joke_id is None
