from decimal import Decimal

from mb_std import number_with_separator, str_to_list


def test_str_to_list():
    data = """
A # 1
b

c
b
    """
    assert str_to_list(data) == ["A # 1", "b", "c", "b"]
    assert str_to_list(data, lower=True, remove_comments=True, unique=True) == ["a", "b", "c"]


def test_number_with_separator():
    assert number_with_separator(123.123) == "123.12"
    assert number_with_separator(123123) == "123_123"
    assert number_with_separator(Decimal("1231234")) == "1_231_234"
