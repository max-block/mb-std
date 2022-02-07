from mb_std import Result


def test_is_ok():
    assert Result().is_ok()
    assert not Result().is_error()

    assert Result(ok=1).is_ok()
    assert not Result(ok=1).is_error()

    assert Result(error="bla").is_error()
    assert not Result(error="bla").is_ok()

    r = Result(ok="123", data=1)
    assert r.replace_ok(int(r.ok)).ok == 123
    assert r.replace_ok(int(r.ok)).data == 1

    r = Result(error="123", data=1)
    assert r.replace_error("abc").error == "abc"
    assert r.replace_error("abc").data == 1


def test_ok_or_error():
    assert Result(ok=123, error="bla bla").ok_or_error == "bla bla"
    assert Result(ok=123).ok_or_error == 123


def test_result_str():
    res = Result(ok=123)
    assert res.__str__() == "{'ok': 123, 'error': None, 'data': None}"


def test_new_ok():
    res = Result.new_ok(123)
    assert res.ok == 123
    assert res.data is None

    res = Result.new_ok(123, {"a": 1})
    assert res.ok == 123
    assert res.data == {"a": 1}


def test_new_result():
    res = Result.new_error("bla")
    assert res.error == "bla"
    assert res.data is None

    res = Result.new_error("bla", {"a": 1})
    assert res.error == "bla"
    assert res.data == {"a": 1}
