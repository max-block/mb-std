import pytest
from pymongo.database import Database

from mb_std import get_dotenv
from mb_std.mongo import MongoConnection


@pytest.fixture
def mongo_database() -> Database:
    conn = MongoConnection.connect("mongodb://localhost/mb-std__test")
    conn.client.drop_database(conn.database)

    conn = MongoConnection.connect("mongodb://localhost/mb-std__test")
    return conn.database


@pytest.fixture
def telegram_token() -> str:
    return get_dotenv("TELEGRAM_TOKEN")  # type: ignore


@pytest.fixture
def telegram_chat_id() -> int:
    return int(get_dotenv("TELEGRAM_CHAT_ID"))  # type: ignore
