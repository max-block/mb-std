from mb_std.dotenv import dotenv


def test_dotenv():
    assert dotenv("TEST_DOTENV") == "777"
