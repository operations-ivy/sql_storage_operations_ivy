import pytest
import datetime
from sql_storage_operations_ivy.sqlite_storage import SqliteStorage


@pytest.fixture
def storage():
    storage = SqliteStorage(":memory:")
    create_table_sql = """
    CREATE TABLE chuck (
        id TEXT PRIMARY KEY,
        category TEXT,
        value TEXT,
        timestamp DATETIME
    )
    """
    storage.cursor.execute(create_table_sql)
    storage.conn.commit()
    yield storage
    storage.close_connection()


def test_insert_and_read_all_jokes(storage):
    storage.insert_joke("123", "funny", "Why did the chicken cross the road?")
    jokes = storage.read_all_jokes()
    assert len(jokes) == 1
    assert jokes[0][0] == "123"
    assert jokes[0][1] == "funny"
    assert jokes[0][2] == "Why did the chicken cross the road?"
    assert isinstance(jokes[0][3], (str, datetime.datetime))


def test_check_for_duplicate_true(storage):
    storage.insert_joke("456", "dad", "I'm on a seafood diet. I see food and I eat it.")
    is_duplicate = storage.check_for_duplicate("456", "I'm on a seafood diet. I see food and I eat it.")
    assert is_duplicate is True


def test_check_for_duplicate_false(storage):
    storage.insert_joke("789", "tech", "There are 10 types of people in the world...")
    is_duplicate = storage.check_for_duplicate("999", "This is not a joke.")
    assert is_duplicate is False


def test_get_joke_id_by_value_found(storage):
    storage.insert_joke("abc", "classic", "Knock knock.")
    joke_id = storage.get_joke_id_by_value("Knock knock.")
    assert joke_id[0] == "abc"


def test_get_joke_id_by_value_not_found(storage):
    joke_id = storage.get_joke_id_by_value("This joke doesn't exist.")
    assert joke_id is None

