from typing import Optional

import pytest
from pydantic import Field
from pymongo import IndexModel
from pymongo.errors import WriteError

from mb_std.mongo import MongoCollection, MongoModel, ObjectIdStr, parse_str_index_model


class Data(MongoModel):
    __collection__ = "data"
    __indexes__ = ["!name"]
    id: Optional[ObjectIdStr] = Field(None, alias="_id")
    name: str


def test_wrap_object_id(mongo_database):
    # with wrapper
    class Data1(MongoModel):
        __collection__ = "data1"
        id: Optional[ObjectIdStr] = Field(None, alias="_id")
        name: str

    coll = MongoCollection(Data1, mongo_database)
    assert coll.wrap_object_id

    # without wrapper
    class Data2(MongoModel):
        __collection__ = "data2"
        id: Optional[int] = Field(None, alias="_id")
        name: str

    coll = MongoCollection(Data2, mongo_database, False)
    assert not coll.wrap_object_id


def test_mongo_model_init_collection(mongo_database):
    col: MongoCollection[Data] = Data.init_collection(mongo_database)
    col.insert_one(Data(name="n1"))
    col.insert_one(Data(name="n2"))
    assert col.count({}) == 2


def test_schema_validation(mongo_database):
    class Data3(MongoModel):
        __collection__ = "data3"
        id: Optional[int] = Field(None, alias="_id")
        name: str
        value: int

        __validator__ = {"$jsonSchema": {"required": ["name", "value"], "properties": {"value": {"minimum": 10}}}}

    col: MongoCollection[Data3] = Data3.init_collection(mongo_database)
    col.insert_one(Data3(name="n1", value=100))
    with pytest.raises(WriteError):
        col.update_one({"name": "n1"}, {"$set": {"value": 3}})


def test_parse_str_index_model():
    assert IndexModel("k").document == parse_str_index_model("k").document
    assert IndexModel("k", unique=True).document == parse_str_index_model("!k").document
    assert IndexModel([("a", 1), ("b", -1)], unique=True).document == parse_str_index_model("!a,-b").document
