import os
from urllib.parse import urlparse

from dotenv import load_dotenv

from mb_std import FIREFOX_USER_AGENT, hrequest


def test_custom_user_agent():
    user_agent = "moon cat"
    res = hrequest("https://httpbin.org/user-agent", user_agent=user_agent)
    assert user_agent in res.body


def test_json_parse_error():
    res = hrequest("https://httpbin.org")
    assert res.json_parse_error


def test_firefox_user_agent():
    res = hrequest("https://httpbin.org/user-agent", user_agent=FIREFOX_USER_AGENT)
    assert FIREFOX_USER_AGENT in res.body


def test_get_params():
    res = hrequest("https://httpbin.org/get", params={"a": 123, "b": "bla bla"})
    assert res.json["args"]["b"] == "bla bla"


def test_post_method():
    res = hrequest("https://httpbin.org/post", method="post", params={"a": 1}, json_params=True)
    assert res.json["data"] == '{"a": 1}'

    res = hrequest("https://httpbin.org/post", method="POST", params={"a": 1}, json_params=True)
    assert res.json["data"] == '{"a": 1}'


def test_timeout():
    res = hrequest("https://httpbin.org/delay/10", timeout=2)
    assert res.error == "timeout"
    assert res.is_timeout_error()


def test_proxy_error():
    res = hrequest("https://httpbin.org/ip", proxy="https://no-real-domain.org:8888")
    assert res.error == "proxy_error"
    assert res.is_proxy_error()


def test_connection_error():
    res = hrequest("https://httpbin222.org/ip", timeout=2)
    assert res.error.startswith("connection_error")


def test_to_ok():
    res = hrequest("https://httpbin.org/ip")

    assert res.to_ok(res.json).data["http_code"] == res.http_code
    assert res.to_ok(res.json).is_ok()
    assert res.to_ok(res.json).ok == res.json


def test_to_error():
    res = hrequest("https://httpbin222.org/ip")
    assert res.to_error().data["http_code"] == res.http_code
    assert res.to_error().is_error()
    assert res.to_error().error.startswith("connection_error")
    assert res.is_connection_error()

    res = hrequest("https://httpbin222.org/ip")
    assert res.to_error("bla").error == "bla"


def test_proxy():
    load_dotenv()
    proxy_url = os.getenv("PROXY", "")

    proxy = urlparse(proxy_url)

    res = hrequest("https://httpbin.org/ip", proxy=proxy_url)
    assert proxy.hostname in res.json["origin"]
