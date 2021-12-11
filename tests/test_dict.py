from mb_std import replace_empty_values


def test_replace_empty_values():
    data = {"a": None, "b": 0, "c": [], "d": 111}
    defaults = {"a": "bla", "b": 1, "c": [1, 2, 3]}
    replace_empty_values(data, defaults)
    assert data == {"a": "bla", "b": 1, "c": [1, 2, 3], "d": 111}


# def test_md():
#     a = "bla"
#     b = 1
#     res = md(a, b)
#     # print("ss", res)
#     assert res == {"a": a, "b": b}
#
#     d1, d2 = md(b, a, b), md(b, a, b)
#     assert d1 == d2
#
#     res = md(a, b, c=777)
#     assert res == {"a": a, "b": b, "c": 777}
