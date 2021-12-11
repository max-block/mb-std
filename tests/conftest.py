import pytest
from pymongo.database import Database

from mb_std.mongo import MongoConnection


@pytest.fixture
def mongo_database() -> Database:
    conn = MongoConnection.connect("mongodb://localhost/mb-commons__test")
    conn.client.drop_database(conn.database)

    conn = MongoConnection.connect("mongodb://localhost/mb-commons__test")
    return conn.database
